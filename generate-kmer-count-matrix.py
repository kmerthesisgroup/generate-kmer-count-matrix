#!/bin/python3

import argparse
import random
import subprocess
import os
import math
import shutil
from typing import Dict, List


def reverse_compliment(kmer: str) -> str:
    compliment_dict = {"A":"T", "C":"G", "G":"C", "T":"A"}
    return str.join("", map(lambda x:compliment_dict[x], reversed(kmer)))

def sample_kmer(length: int) -> str:
    alphabet = "ACGT"
    k1 = str.join("", random.choices(alphabet,k=length))
    k2 = reverse_compliment(k1)
    if k1<k2:
        return k1
    return k2

def sample_kmers(length: int, num_sample: int) -> List[str]:
    return [sample_kmer(length) for _ in range(num_sample)]

def create_taxa_file(args, samples: List[str]):
    with open(args.taxa_file, "w") as f:
        for i in range(len(samples)):
            f.writelines([">{}\n".format(i), samples[i], "\n"])

def create_species_file(args):
    species = []
    for fastafile in args.species_files:
        with open(fastafile, "r") as f:
            species.append(f.readline()[1:].strip())
    
    with open(args.species_file, "w") as out:
        out.writelines([f"{len(species)}\n", " ".join(species), "\n"])

def get_jf_filepath(fastafile: str, jf_storage_dir: str) -> str:
    base_name = os.path.basename(fastafile).split(".")[0]
    return os.path.join(jf_storage_dir, base_name+".jf")

def get_jf_dump_filepath(fastafile: str, jf_storage_dir: str) -> str:
    base_name = os.path.basename(fastafile).split(".")[0]
    return os.path.join(jf_storage_dir, base_name+".jf.dump")

def build_count_command(taxa_file: str, fastafile : str, kmerlen: int, num_threads: int, jf_storage_dir:str) -> str:
    filesize = os.stat(fastafile).st_size
    
    jf_file = get_jf_filepath(fastafile, jf_storage_dir)
    jellyfish_count = f"time jellyfish count -m {kmerlen} -s {filesize} -t {num_threads} -C {fastafile} --if {taxa_file} -o {jf_file}"
    return jellyfish_count

def build_dump_command(fastafile: str, jf_storage_dir: str) -> str:
    jf_file = get_jf_filepath(fastafile, jf_storage_dir)
    dump_file = get_jf_dump_filepath(fastafile, jf_storage_dir)
    jellyfish_dump = f"time jellyfish dump {jf_file} > {dump_file}"
    return jellyfish_dump


def build_query_command(kmer: str, jf_file: str) -> str:
    return f"time jellyfish query {jf_file} {kmer}"

def create_jf_file(args, fastafile):
    extenstion = fastafile.split(".")[-1]  
    if extenstion not in ["jf", "dump"]:
        cmd = build_count_command(args.taxa_file, fastafile, args.kmerlen, 10, args.jf_storage_dir)
        print(f"+ {cmd}")
        subprocess.check_output(cmd, shell=True)
    elif extenstion == "jf":
        shutil.copy(fastafile, get_jf_filepath(fastafile, args.jf_storage_dir))

def create_dump_file(args, fastafile):
    extenstion = fastafile.split(".")[-1]  
    if extenstion != "dump":
        cmd = build_dump_command(fastafile, args.jf_storage_dir)
        print(f"+ {cmd}")
        subprocess.check_output(cmd, shell=True)
    elif extenstion == "dump":
        shutil.copy(fastafile, get_jf_dump_filepath(fastafile, args.jf_storage_dir))

def parse_dump_file(dump_file)->Dict[str, int]:
    with open(dump_file, "r") as f:
        lines = f.readlines()
        cnt = [ int(line.strip()[1:]) for line in lines[::2] ]
        kmers = [ line.strip() for line in lines[1::2] ]
        return { k:v for k,v in zip(kmers, cnt)}

def read_kmer_count(dump_parse: Dict[str, int], samples: List[str]) -> List[int]: 
    return [ dump_parse[kmer] if kmer in dump_parse else 0 for kmer in samples ]
    
def create_count_matrix_file(args, cnt_matrix):
    with open(args.count_matrix_file, "w") as f:
        f.writelines([str(len(args.species_files)) + " " + str(args.num_sample), "\n"])
        for i in range(len(cnt_matrix)):
            s = [ str(cnt)+" " for cnt in cnt_matrix[i]]
            s[-1] = s[-1].strip()
            s.append("\n")
            f.writelines(s)

def create_entropy_file(args, cnt_matrix):
    entropy = 0.0
    num_species = len(cnt_matrix)
    for i in range(args.num_sample):
        one = sum([cnt_matrix[j][i] >0 for j in range(num_species)])
        zero = num_species - one
        
        if zero > 0:
            entropy += -zero/num_species*math.log(zero/num_species)

        if one > 0:
            entropy += -one/num_species*math.log(one/num_species)
    
    with open(args.entropy_file, "w") as entropy_file:
        entropy_file.writelines([str(entropy), "\n"])


def main(args):
    if args.seed_zero:
        random.seed(0)

    samples = sample_kmers(args.kmerlen, args.num_sample)
    create_taxa_file(args, samples)

    create_species_file(args)

    args.created_jf_dir = False
    if not os.path.isdir(args.jf_storage_dir):
        args.created_jf_dir = True
    os.makedirs(args.jf_storage_dir, exist_ok=True)
    
    cnt_matrix = []
    for fastafile in args.species_files:
        create_jf_file(args, fastafile)
        create_dump_file(args, fastafile)
        dump_map = parse_dump_file(get_jf_dump_filepath(fastafile, args.jf_storage_dir))
        cnts = read_kmer_count(dump_map, samples)
        cnt_matrix.append(cnts)

    create_count_matrix_file(args, cnt_matrix)
    create_entropy_file(args, cnt_matrix)
    cleanup(args)

def cleanup(args):
    if not args.keep_jf:
        if args.created_jf_dir:
            os.rmdir(args.jf_storage_dir)
        else:
            for fastafile in args.species_files:
                jf_file = get_jf_filepath(fastafile, args.jf_storage_dir)
                os.remove(jf_file)

                dump_file = get_jf_dump_filepath(fastafile, args.jf_storage_dir)
                os.remove(dump_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--kmerlen", action="store", required=True,type=int, help="length of the kmers to count")
    parser.add_argument("--num-sample", action="store", required=True, type=int, help="number of samples to use")
    parser.add_argument("--seed-zero", action="store_true", default=True, 
                        help="whether or not to seed with zero, by default set to true") 

    parser.add_argument("--keep-jf", action="store_true", default=False, help="whether or not to keep .jf files")
    parser.add_argument("--jf-storage-dir", action="store", default="./", help="directory to store .jf files, if generated")
    
    parser.add_argument("--taxa-file", action="store", default="taxafile.txt", help="taxafile")
    parser.add_argument("--count-matrix-file", action="store", default="count-matrix.txt", help="count-matrix file")
    parser.add_argument("--entropy-file", action="store", default="entropy.txt", help="entropy file")
    parser.add_argument("--species-file", action="store", default="species.txt", help="name of species file")

    parser.add_argument("species_files", nargs="+", help="fasta files files to generate kmer-count-matrix-from") 

    args = parser.parse_args()
    main(args)


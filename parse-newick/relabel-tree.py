#!/bin/python3

import argparse
import sys

from typing import List, Tuple

def parse_tree(args) -> List[Tuple[int, int, str]]:
    edges = []
    with open(args.treefile) as treefile:
        species_cnt = int(treefile.readline())
        args.species_cnt = species_cnt

        edge_cnt = 2*species_cnt - 2
        for _ in range(edge_cnt):
            line = treefile.readline().strip()
            line = line.split()
            edges.append((int(line[0]),int(line[1]),line[2]))
    return edges

def parse_relabelings(args) -> List[int]:
    with open(args.species_file, "r") as old:
        cnt = int(old.readline().strip())
        old_species = ' '.join(old.readlines()).strip().split()
        if cnt != len(old_species):
            print("Error: Number of species in file {} doesn't match with actual number of species".format(args.species_file), 
                  file=sys.stderr)
            exit(-1)
    
        
    with open(args.relabel_file, "r") as new:
        cnt = int(new.readline().strip())
        new_species = ' '.join(new.readlines()).strip().split()
        if cnt != len(new_species):
            print("Error: Number of species in file {} doesn't match with actual number of species".format(args.relabel_file), 
                  file=sys.stderr)
            exit(-1)

    if len(old_species) != len(new_species):
        print("Error: Number of species in both files need to be the same", file=sys.stderr)
        exit(-1)

    permutation = [0 for _ in range(len(old_species))]
    for i in range(len(permutation)):
        try:
            permutation[i] = new_species.index(old_species[i])
        except ValueError:
            print("{} not found in relalled-file".format(old_species[i]), file=sys.stderr)
    return permutation
    
def get_relabelled_edges(args, edges, permutation) -> List[Tuple[int, int, str]]:
    new_edges = []
    for e in edges:
        u = e[0]
        v = e[1]
        if 1<= u <= args.species_cnt:
            u = permutation[u-1] + 1
        
        if 1<= v <= args.species_cnt:
            v = permutation[v-1] + 1

        new_edges.append((u, v, e[2]))
    
    return new_edges

def create_new_treefile(args, new_edges):
    with open(args.output, "w") as treefile:
        treefile.writelines([str(args.species_cnt), "\n"])
        for e in new_edges:
            treefile.writelines(["{} {} {}\n".format(e[0], e[1], e[2])])


def main(args):
    edges = parse_tree(args)
    permutation = parse_relabelings(args)
    relabled_tree = get_relabelled_edges(args, edges, permutation)
    create_new_treefile(args, relabled_tree)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--treefile", required=True, help="name of treefile")
    parser.add_argument("--species-file", required=True, help="name of species file")
    parser.add_argument("--relabel-file", required=True, help="name of relabelling species file")
    parser.add_argument("--output", default="relabled-tree.txt", help="name of output file")

    args = parser.parse_args()

    main(args)


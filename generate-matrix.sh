#!/bin/bash 

dir="$1-$2-$3"

mkdir -p $dir

time ../generate-kmer-count-matrix.py --kmerlen $2 --num-sample $3 --seed-zero --keep-jf --jf-storage-dir $dir/jf-dir/ --taxa-file $dir/taxafile.txt --count-matrix-file $dir/count-matrix.txt --entropy $dir/entropy.txt --species-file $dir/species-file.txt $(echo $(ls data/*))

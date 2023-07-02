#!/bin/bash

set -xe


MATRIX_DIR="$1-$2-$3"
NEWICK_DIR=newick


for treefile in $(ls "$NEWICK_DIR")
do 
	echo $treefile 
	basename=${treefile%.newick}
	dir="$basename-$1-$2-$3"
	mkdir -p "$dir"
	cd "$dir"
	../../parse-newick/newick "../$NEWICK_DIR/$treefile"
	../../parse-newick/relabel-tree.py --treefile "out.tree" --species-file "species_file" --relabel-file "../$MATRIX_DIR/species-file.txt" --out final.tree
	../../merge/merge.out final.tree "../$MATRIX_DIR/count-matrix.txt" > "final_tree.txt" 
	cd ..
done


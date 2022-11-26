#!/bin/bash 

NEWICK_DIR=newick

for treefile in $(ls "$NEWICK_DIR")
do
	echo "$treefile"
	basename="${treefile%.newick}"
	rm -r $basename-* 
done

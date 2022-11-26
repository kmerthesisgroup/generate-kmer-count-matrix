# `merge`

## Usage 
```
merge.out [tree_file_path transposed_count_matrix_file_path]
```

## Output
`stdout`

## Format of transposed_count_matrix_file_path
It is the output of parse-count-matrix.out for a count-matrix-file and a given species file
num_species number_of_sites
c11        c12       c13          c1N
c21        ...       ...          c2N 
...        ...       ...          ...
...        ...       ...          ...
...        ...       ...          ...
cK1        ...       ...          cKN 



## Format of Treefile
output of parsing the newick tree.

## Format of output 
concatination of the files to `stdout`

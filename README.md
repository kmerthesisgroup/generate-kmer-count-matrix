## Dependencies
- `flex`
- `bison`
- `jellyfish`
- `bash`
- `python3`
- `curl`
- `g++`
- `unzip`
## How to Use

### Download Dependencies
In debian we can use the following command:
```
sudo apt-get install flex bison jellyfish g++ python3 curl unzip 
```

### Build Executables
```
cd merge
./build.sh
cd ..
cd parse-newick
./build.sh
cd ..
```

### Prepare Workspace
Create a new directory in the root of the project directory and copy the `run.sh` & `generate-matrix.sh` and `clean.sh` scripts.
```
mkdir plant
cd plant 
cp ../run.sh ./ 
cp ../generate-matrix.sh ./
cp ../clean.sh ./
```

### Copy Data into the workspace
Copy the fasta files into a directory named `data` in the workspace.
The newick files go into a directory called `newick` in the workspace.

### Generate Kmer-count-matrix 
```
./generate-matrix.sh species-name length-of-kmer number-of-samples
```
This will create a folder with the name `{species-name}-{length-of-kmer}-{number-of-samples}` which will contain the kmer-count-matrix and other files.

### Create Trees 
To generate the tree files for all topologies in the newick folder, run:
```
./run species-name kmer-length number-of-samples
```
It will generate one directory for each newick tree in the `newick` directory.

## Example Directories
We have added three example directories, `plant`, `fish` and `ecoli`.
Both of them have a `newick` directory and a download script for the `data` directory.

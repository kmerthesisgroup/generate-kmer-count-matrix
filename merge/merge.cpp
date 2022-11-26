#include <cstdlib>
#include <ios>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;


string tree_file_path = "out.tree";
string matrix_file_path = "transposed.txt";

int fail = 0;

int main(int argc,char** argv) {
	if(argc!=3 && argc!=1) {
		cerr << "Usage: " << "merge.out [tree_file_path count_matrix_file_path]" << endl;
		exit(1);
	} else if(argc==3){
		tree_file_path = string(argv[1]);
		matrix_file_path = string(argv[2]);
	}

	fstream tree_file;
	tree_file.open(tree_file_path,ios_base::in);
	if(!tree_file.is_open()) {
		cerr << "Failed to open tree_file: " << tree_file_path << endl;
		fail = 1;	
	}

	fstream matrix_file;
	matrix_file.open(matrix_file_path,ios::in);
	if(!matrix_file.is_open()) {
		cerr << "Failed to open count_matrix_file: " << matrix_file_path << endl;
		fail=1;
	}

	if(fail) exit(1);
	
	int species_count;
	tree_file >> species_count;

	int temp, number_of_sites;
	matrix_file >> temp >> number_of_sites;

	if(temp!=species_count) {
		cerr << "species_count doesn't match\n";
		cerr << "species_count is " << species_count << "in tree_file but " << temp << "count_matrix_file" << endl;
		exit(1);
	}

	cout << species_count << "\n";
	cout << number_of_sites << endl;
	cout << "-1 -1 -1\n"; 

	//print tree topology
	int number_of_nodes = species_count*2-1;
	for (int i=0;i<number_of_nodes-1;i++) {
		int u,v;
		double l;
		tree_file >> u >> v >> l;
		cout << u << " " << v<< " " << l << "\n"; 
	}

	tree_file.close();


	for(int i=0;i<species_count;i++) {
		for(int j=0;j<number_of_sites;j++) {
			long long temp;
			matrix_file >> temp;
			cout << temp << " ";
		}
		cout << "\n";
	}
	matrix_file.close();

}

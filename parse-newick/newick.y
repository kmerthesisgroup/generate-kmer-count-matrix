%{

#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <fstream>
#include "edge.hpp"
using namespace std;

extern FILE* yyin;
extern int yylineno;
extern int yylex(void);

int node_counter = 0;
vector<string> label_map;
vector<int> leaves;
int root;

vector<vector<edge>> adjList;
vector<int> relabeled_nodes;
vector<int> inverse_relabeled_nodes;

void yyerror(char const* s); 

%}

%union {
	vector<edge>* branch_set;
	int node;
	edge branch;
	double branch_length;
	char* text;
}

%code requires {
	#include "edge.hpp"
}


%locations
%define parse.error verbose

%token <text> WORD

%start TREE;

%type <node> SUB_TREE;
%type <node> LEAF;
%type <node> INTERNAL_NODE;
%type <branch_set> BRANCH_SET;
%type <branch> BRANCH;
%type <text> NAME;
%type <branch_length> BRANCH_LENGTH;



%%


TREE: SUB_TREE ';' {
	cerr << "TREE -> SUB_TREE ;" << endl;
	root = $1;
	cerr << "TREE -> "<< root  << " ;" << endl;
}
;

SUB_TREE: LEAF {
	cerr << "SUB_TREE -> LEAF" << endl;
	$$=$1;
	cerr << "SUB_TREE -> " << label_map[$$] << endl;
	cerr << "SUB_TREE -> " << $$ << endl << endl;
	
}
| INTERNAL_NODE {
	cerr << "SUB_TREE -> INTERNAL_NODE" << endl;
	$$=$1;
	cerr << "SUB_TREE -> " << label_map[$$] << endl;
	cerr << "SUB_TREE -> " << $$ << endl << endl;
}
;

LEAF: NAME {
	string s($1);
	delete[] $1;
	cerr << "LEAF -> NAME" << endl;
	cerr << "LEAF -> " << s << endl;
	$$=node_counter++;
	label_map.push_back(s);
	leaves.push_back($$);
	adjList.push_back(vector<edge>());
	cerr << "LEAF -> " << $$ << endl << endl;
}
;

INTERNAL_NODE: '(' BRANCH_SET ')' NAME {
	cerr << "INTERNAL_NODE -> ( BRANCH_SET ) NAME" << endl;
	string s($4);
	delete[] $4;
	$$=node_counter++;
	adjList.emplace_back(*($2));
	label_map.push_back(s);
	for(int i=0;i<adjList[$$].size();i++) {
		adjList[$$][i].u = $$;
		int v = adjList[$$][i].v;
		double length = adjList[$$][i].length;
		adjList[v].push_back({v,$$,length});
	}

	cerr << "INTERNAL_NODE -> ( ";

	for(int i=0;i<adjList[$$].size();i++) {
		cerr << adjList[$$][i].v << " ";
	}

	cerr << ") " << $$ << endl << endl;

}
;

BRANCH_SET: BRANCH {
	cerr << "BRANCH_SET -> BRANCH" << endl;
	$$ = new vector<edge>();
	$$->push_back($1);
	cerr << "BRANCH_SET -> {(" << (*$$)[0].u << ", " << (*$$)[0].v << ", " << (*$$)[0].length << ")}" << endl << endl;
}
| BRANCH ',' BRANCH_SET {
	cerr << "BRANCH_SET -> BRANCH , BRANCH_SET" << endl;
	$$ = $3;
	$$->push_back($1); 
	cerr << "BRANCH_SET -> {(" << (*$$)[0].u << ", " << (*$$)[0].v << ", " << (*$$)[0].length << ") ";
	for(int i=1;i<$$->size();i++) {
		cerr << "," << "(" << (*$$)[i].u << ", " << (*$$)[i].v << ", " << (*$$)[i].length << ") ";
	}
	cerr << "}" << endl << endl;
}
;

BRANCH: SUB_TREE BRANCH_LENGTH {
	cerr << "BRANCH -> SUB_TREE BRANCH_LENGTH" << endl;
	$$.u = -1;
	$$.v = $1;
	$$.length = $2;
	cerr << "BRANCH -> (" << $$.u << ", " << $$.v << ", "
	<< $$.length << ")" << endl << endl;
}
;

NAME: %empty {
	cerr << "NAME -> EMPTY" << endl;
	$$ = new char[1];
	$$[0] = '\0';
	cerr << "NAME -> " << $$ << endl << endl;
}
| WORD {
	cerr << "NAME -> WORD" << endl;
	$$ = $1;
	cerr << "NAME -> " << $$ << endl << endl;
}
;

BRANCH_LENGTH: %empty {
	cerr << "BRANCH_LENGTH -> EMPTY " << endl;
	$$ = -1;
	cerr << "BRANCH_LENGTH -> " << $$ << endl << endl;
}
| ':' WORD {
	cerr << "BRANCH_LENGTH -> : WORD " << endl;
	string s($2);
	delete[] $2;
	$$ = stod(s);
	cerr << "BRANCH_LENGTH -> : " << $$ << endl << endl;
}
;


%%

void relabel() {
	int number_of_leaves = leaves.size();
	int number_of_nodes = adjList.size();
	
	set<int> leaf_set;
	for(auto v:leaves) leaf_set.insert(v);
	
	int leaf_counter = 0;
	int internal_node_counter = 0;

	relabeled_nodes.resize(number_of_nodes);
	inverse_relabeled_nodes.resize(number_of_nodes);
	for(int i=0;i<number_of_nodes;i++) {
		if(leaf_set.find(i)!=leaf_set.end()) {
			relabeled_nodes[i]=++leaf_counter;
			inverse_relabeled_nodes[leaf_counter]=i;
		}
		else if(i==root) {
			relabeled_nodes[i]=0;
			inverse_relabeled_nodes[0]=i;
		} else {
			relabeled_nodes[i] = number_of_leaves+(++internal_node_counter);
			inverse_relabeled_nodes[number_of_leaves+internal_node_counter]=i;
		}
	}
}

string species_file = "species_file";

void print_leaf_node_names() {
	fstream outfile;
	outfile.open(species_file,std::ios_base::out);

	outfile << leaves.size() << "\n";
	cerr << leaves.size() << endl;
	for(int i=1;i<=leaves.size();i++) {
		outfile << label_map[inverse_relabeled_nodes[i]] << " ";
		cerr << label_map[inverse_relabeled_nodes[i]] << " ";
	}
	outfile << endl;
	cerr << endl;

	outfile.close();
}

string tree_out = "out.tree";
void print_tree() {
	int number_of_leaves = leaves.size();
	int number_of_nodes = adjList.size();
	
	fstream outfile;
	outfile.open(tree_out,std::ios_base::out);

	cerr << number_of_leaves << endl;
	outfile << number_of_leaves << "\n";


	for(int i=0;i<number_of_nodes;i++) {
		for(auto &e: adjList[i]) {
			if(relabeled_nodes[e.u]<relabeled_nodes[e.v]) {
				cerr << relabeled_nodes[e.u] << " " << relabeled_nodes[e.v] << " " << e.length << endl;
				outfile << relabeled_nodes[e.u] << " " << relabeled_nodes[e.v] << " " << e.length << "\n";
			}
		}
	}
	outfile.close();

}

int main(int argc, char** argv) {
	FILE* fp = NULL;	
	if(argc==2) {
		fp = fopen(argv[1],"r");
		if(!fp) {
			cerr << "ERROR opening file " << argv[1] << endl;
			exit(1);
		}
		yyin = fp;
	} else if(argc>2) {
		cerr << "USAGE: newick treefile" << endl;
		exit(0);
	}

	yyparse();
	if(fp) fclose(fp);
	relabel();
	print_leaf_node_names();
	print_tree();
}

void yyerror(char const* s) {
    fprintf(stderr, "%s\n", s);
}


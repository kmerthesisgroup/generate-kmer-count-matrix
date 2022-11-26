#!/bin/bash

g++ -std=c++17 -o edge.o edge.cpp -c
bison -d newick.y 
flex newick.l
g++ -std=c++17 -o newick-lex.o lex.yy.c -c
g++ -std=c++17 -o newick newick.tab.c newick-lex.o edge.o 


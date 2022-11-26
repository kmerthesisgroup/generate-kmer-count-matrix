%option noyywrap
%option yylineno

%{
#include <stdio.h>
#include <vector>
using namespace std;
#include "newick.tab.h"

#define YY_USER_ACTION {yylloc.first_column = column_offset; column_offset+=yyleng; yylloc.first_line = yylloc.last_line = yylineno; yylloc.last_column=column_offset;}


int curr_line = 0;
int column_offset = 1;


%}


%%
[ \t\b\f\n\r\v] {}
[^,:;\(\) \t\b\f\n\r\v][^,:;\(\)]* {
	yylval.text = new char[sizeof(yytext)+1];
	strcpy(yylval.text,yytext);
	return WORD;
	//printf("NAME: %s\n",yytext);
}
. {return yytext[0];}
%%

/*int main() {
	yylex();
}*/ 

#include <stdlib.h>
#include <stdint.h>

/*
 Écris dans un fichier le block de texte contenu dans l'input.
 @param filename nom du fichier
 @param x  
 @param input block de texte à écrire dans le fichier 
*/
void write_in_file(char *filename, int x, char *input);

uint64_t findSize(char *filename);

/*
Lit le block de texte de maximun de 16 caractères 
dépuis un fichier passer en paramètre et le copie dans b
@param filename: le nom du fichier
@param start: position à laquelle on commence à lire le fichier
*/
int read_block_n(char *b, char *filename, int start);

int is_text_file(char *filename);

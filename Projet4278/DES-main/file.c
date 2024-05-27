#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "file.h"
#include <stdint.h>

char *choice[] = {"_cypherText.txt", "_plainText.txt"};

void write_in_file(char *filename, int x, char *input)
{
    char *t = malloc(100 * sizeof(*t)), *p = choice[x];
    if (t == NULL)
    {
        printf("Il n’y a pas assez de mémoire \n");
        exit(EXIT_FAILURE);
    }
    strcpy(t, filename);
    strcat(t, p);
    FILE *f;
    if ((f = fopen(t, "a+")) != NULL)
    {
        fwrite(input, sizeof(char), strlen(input), f);
    }
    else
    {
        printf("File not found (%s)", filename);
        exit(0);
    }
    fclose(f);
    free(t);
}

uint64_t findSize(char *filename)
{
    FILE *fp = fopen(filename, "r");

    if (fp == NULL)
    {
        printf("File not found");
        exit(EXIT_FAILURE);
    }

    fseek(fp, 0, SEEK_END);
    uint64_t res = ftell(fp);
    fclose(fp);

    return res;
}

int read_block_n(char *b, char *filename, int start)
{
    FILE *f;
    char ch;
    int n = 0, r=0;

    if ((f = fopen(filename, "r")) != NULL)
    {
        fseek(f, sizeof(char) * start, SEEK_SET);

        while (n < 16 && (ch != EOF))
        {
            ch = fgetc(f);
            if (ch != '\n')
            {
               b[n] = ch;
            n++;
            }else{
                r =1;
            }
            
        }
        if (n < 16)
            b[n - 1] = '\0';
    }
    else
    {
        printf("File not found (%s)", filename);
        exit(0);
    }
    fclose(f);

    return r;
}

int is_text_file(char *filename)
{
    char *loc = malloc(sizeof(*loc) * 4);
    loc = strrchr(filename, '.');

    if (loc == NULL)
        return -1;

    return strcmp(loc, ".txt");
}
/*int main(int argc, char **argv)
{
    // char *y = malloc(16 * sizeof(*y)); printf("%ld",strlen(y));
    printf("%s", read_block("text.txt", 0));
}*/

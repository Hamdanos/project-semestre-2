#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "des.h"
#include "msg.h"
#include "file.h"
#include <stdint.h>
#define ENCRYPT "1"
#define DECRYPT "2"

int encrypt_or_decrypt();
char *get_text_path(int v, int c);

int main(int argc, char **argv)
{
    printf("CHIFFREMENT DES\n");

    // title
    start_des();

    char **ar = malloc(3 * sizeof(*ar));
    int c = encrypt_or_decrypt();
    printf("\n");

    char l[10];
    sprintf(l, "%d", c);
    ar[0] = l;
    ar[1] = get_text_path(1, c);
    ar[2] = get_text_path(0, c);
    printf("\n");

    ar[1][strlen(ar[1]) - 1] = '\0';
    ar[2][strlen(ar[2]) - 1] = '\0';

    argv[1] = ar[0];
    argv[2] = ar[1];
    argv[3] = ar[2];

    // On teste si les deux fichiers sont des fichiers texte
    if ((is_text_file(argv[2]) != 0) || (is_text_file(argv[3]) != 0))
    {
        printf("You should provide text file\n");
        exit(0);
    }

    // Récupération de la clé
    char r[16];
    read_block_n(r, argv[3], 0);
    uint64_t key = strtoul(r, NULL, 16);

    if (0 == strcmp(argv[1], ENCRYPT))
    {


        char *file =  argv[2];
        printf("\tChiffrement du fichier: %s\n\tveuillez patienter....", argv[2]);
        for (uint64_t i = 0; i < findSize(file); i = i + 16)
        {
            char a[17];
            if (read_block_n(a, file, i))
                i++;
            if (strcmp(a, "") == 0)
            {
                continue;
            }
            sprintf(a, "%lx", encrypt(strtoul(a, NULL, 16), key_schedule(key)));
            write_in_file(file, 0, a);
        }
        printf("\n\tChiffrement du fichier: %s terminé\n", argv[2]);
    }
    else if (0 == strcmp(argv[1], DECRYPT))
    {

        // Déchiffrement
        printf("\tDéchiffrement du fichier: %s\n\tveuillez patienter....", argv[2]);
        for (uint64_t i = 0; i < findSize(argv[2]); i = i + 16)
        {
            char a[17];
            read_block_n(a, argv[2], i);
            sprintf(a, "%016lx", decrypt(strtoul(a, NULL, 16), key_schedule(key)));
            write_in_file(argv[2], 1, a);
        }
        printf("\n\tDéchiffrement du fichier: %s terminé\n", argv[2]);
    }

    return EXIT_SUCCESS;
}

int encrypt_or_decrypt()
{
    int x;
    char ligne[800];

    printf("\tQuelle action souhaitez vous effectuer ?\n");
    printf("\t\t1. Chiffrer un fichier texte\n");
    printf("\t\t2. Déchhiffrer un fichier texte\n");
    printf("\tEntrez le numéro de l'action choisi:");
    fgets(ligne, 80, stdin);
    sscanf(ligne, "%1d", &x);

    while (x != 1 && x != 2)
    {
        printf("\tErreur, le numéro (%d) ne correspond à aucune action.\n", x);
        printf("\tEntrez le numéro de l'action choisie:");
        fgets(ligne, 80, stdin);
        sscanf(ligne, "%1d", &x);
    }

    return x;
}

char *get_text_path(int v, int c)
{
    char *p = malloc(100 * sizeof(*p));

    if (v)
    {
        if (c == 1)
            printf("\tEntrez le chemin du fichier contenant le texte à chiffrer: ");

        if (c == 2)
            printf("\tEntrez le chemin du fichier contenant le texte à déchiffrer: ");
    }
    else
    {
        printf("\tEntrez le chemin du fichier contenant la clé de chiffrement: ");
    }
    fgets(p, 90, stdin);

    return p;
}
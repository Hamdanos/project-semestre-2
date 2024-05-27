#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "binaryUtil.h"

char *representationIn64Bits(uint64_t x)
{
    char *ou;
    char in[2];  // Taille suffisante pour stocker un caractère plus le caractère nul

    if ((ou = malloc(65 * sizeof(*ou))) == NULL)  // 64 bits plus le caractère nul
    {
        printf("Il n’y a pas assez de mémoire\n");
        exit(EXIT_FAILURE);
    }
    *ou = '\0';

    for (unsigned char i = 0; i < 64; i++)
    {
        unsigned char p = (x >> (63 - i)) & LSB64;  // Corrected the shift and mask
        sprintf(in, "%d", p);
        strcat(ou, in);
    }
    return ou;
}

char *representationIn32Bits(uint32_t x)
{
    char *ou;
    char in[2];  // Taille suffisante pour stocker un caractère plus le caractère nul

    if ((ou = malloc(33 * sizeof(*ou))) == NULL)  // 32 bits plus le caractère nul
    {
        printf("Il n’y a pas assez de mémoire\n");
        exit(EXIT_FAILURE);
    }
    *ou = '\0';

    for (unsigned char i = 0; i < 32; i++)
    {
        unsigned char p = (x >> (31 - i)) & LSB32;  // Corrected the shift and mask
        sprintf(in, "%d", p);
        strcat(ou, in);
    }
    return ou;
}

char *representationIn48Bits(uint64_t x)
{
    char *ou;
    char in[2];  // Taille suffisante pour stocker un caractère plus le caractère nul

    if ((ou = malloc(49 * sizeof(*ou))) == NULL)  // 48 bits plus le caractère nul
    {
        printf("Il n’y a pas assez de mémoire\n");
        exit(EXIT_FAILURE);
    }
    *ou = '\0';

    for (unsigned char i = 0; i < 48; i++)
    {
        unsigned char p = (x >> (47 - i)) & LSB48;  // Corrected the shift and mask
        sprintf(in, "%d", p);
        strcat(ou, in);
    }
    return ou;
}

char *representationIn6Bits(uint8_t x)
{
    char *ou;
    char in[2];  // Taille suffisante pour stocker un caractère plus le caractère nul

    if ((ou = malloc(7 * sizeof(*ou))) == NULL)  // 6 bits plus le caractère nul
    {
        printf("Il n’y a pas assez de mémoire\n");
        exit(EXIT_FAILURE);
    }
    *ou = '\0';

    for (unsigned char i = 0; i < 6; i++)
    {
        unsigned char p = (x >> (5 - i)) & LSB6;  // Corrected the shift and mask
        sprintf(in, "%d", p);
        strcat(ou, in);
    }
    return ou;
}

char *representationIn4Bits(uint8_t x)
{
    char *ou;
    char in[2];  // Taille suffisante pour stocker un caractère plus le caractère nul

    if ((ou = malloc(5 * sizeof(*ou))) == NULL)  // 4 bits plus le caractère nul
    {
        printf("Il n’y a pas assez de mémoire\n");
        exit(EXIT_FAILURE);
    }
    *ou = '\0';

    for (unsigned char i = 0; i < 4; i++)
    {
        unsigned char p = (x >> (3 - i)) & LSB4;  // Corrected the shift and mask
        sprintf(in, "%d", p);
        strcat(ou, in);
    }
    return ou;
}

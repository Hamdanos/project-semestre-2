#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "des.h"
#include "msg.h"
#include "binaryUtil.h"
#define DESC "desc.txt"
#include <stdint.h>

struct des_msg msg = {
    "==========================================================================================================\n"
    "=                                       DATA ENCRYPTION STANDART (DES)                                   =\n"
    "==========================================================================================================\n\n",
    "\n\t\t\t\t\tSubKey generation \n"
    "\t\t\t=================================================================\n"};

FILE *fd;

void start_des()
{
    if ((fd = fopen(DESC, "a")) != NULL)
    {
        fprintf(fd, "%s", msg.title);
        fprintf(fd, "%s", msg.key_title);
    }
    else
    {
        printf("File not found (%s)", DESC);
        exit(0);
    }
    fclose(fd);
}

void display_permutation_table(int8_t IP[], unsigned char size, char *tbname)
{

    if ((fd = fopen(DESC, "a")) != NULL)
    {
        fprintf(fd, "\nFINAL PERMUTATION \n");
        fprintf(fd, "\n\t\t\t%s", tbname);
        for (int8_t i = 0; i < size; i++)
        {
            if (!(i % 8))
                fprintf(fd, "\n\t\t\t");
            fprintf(fd, "%3d", IP[i]);
        }
        fprintf(fd, "\n\t\t\t");
    }
    else
    {
        printf("File not found (%s)", DESC);
        exit(0);
    }
    fclose(fd);
}

void display_permutation_tableM(int8_t IP[], unsigned char size, char *tbname)
{

    fprintf(fd, "\n\t\t\t%s", tbname);
    for (int8_t i = 0; i < size; i++)
    {
        if (!(i % 8))
            fprintf(fd, "\n\t\t\t");
        fprintf(fd, "%3d", IP[i]);
    }
    fprintf(fd, "\n\t\t\t");
}

void display_des(uint64_t x, uint64_t *subkey, int8_t b)
{
    uint64_t y = x;
    if (b)
    {
        y = encrypt(x, subkey);
        fprintf(fd, "\n\n\t\t\ty = %lx\n", y);
    }
    else
    {
        fprintf(fd, "\t\t\tx = %lx\n", decrypt(y, subkey));
    }
}

void binary_expansion64(uint64_t x)
{
    if ((fd = fopen(DESC, "a")) != NULL)
    {
        char *plaintext = representationIn64Bits(x);
        fprintf(fd, "\n\t\t\t The binary expansion of ( %lx ) is:", x);
        for (int8_t i = 0; i < strlen(plaintext); i++)
        {
            if (!(i % 8))
                fprintf(fd, "\n\t\t\t");
            fprintf(fd, "%3c", plaintext[i]);
        }
        fprintf(fd, "\n");
    }
    else
    {
        printf("File not found (%s)", DESC);
        exit(0);
    }
    fclose(fd);
}

void binary_expansion64M(uint64_t x)
{
    char *plaintext = representationIn64Bits(x);
    fprintf(fd, "\n\t\t\t The binary expansion of ( %lx ) is:", x);
    for (int8_t i = 0; i < strlen(plaintext); i++)
    {
        if (!(i % 8))
            fprintf(fd, "\n\t\t\t");
        fprintf(fd, "%3c", plaintext[i]);
    }
    fprintf(fd, "\n");
}

void plaintext_init_msg(uint64_t x, uint64_t ip, uint32_t  L, uint32_t  R, int8_t IP[], int8_t b)
{

    if ((fd = fopen(DESC, "a")) != NULL)
    {

        if (b)
        {
            fprintf(fd, "\n\t\t\t\t\tEncryption of (%lx) \n", x);
        }
        else
        {
            fprintf(fd, "\n\t\t\t\t\tDecryption of (%lx) \n", x);
        }
        fprintf(fd, "\t\t\t=================================================================\n");
        fprintf(fd, "\n INITIAL PERMUTATION \n");
        display_permutation_tableM(IP, 64, "The initial permutation, IP.");
        binary_expansion64M(x);
        fprintf(fd, "\n\t\t\tIP(%lx) : %20lx\n", x, ip);
        binary_expansion64M(ip);
        fprintf(fd, "\n");
        fprintf(fd, "\n\n FIESTEL NETWORK \n");
        fprintf(fd, "\t\t\t\t\tROUND 1 \n\n");
        fprintf(fd, "\t\t\tL[0]:%33s\n\t\t\tR[0]:%33s\n", representationIn32Bits(L), representationIn32Bits(R));
    }
    else
    {
        printf("File not found (%s)", DESC);
        exit(0);
    }
    fclose(fd);
}

void display_f_function(uint64_t permutation, uint64_t k, uint64_t E_xor_K, int8_t E[])
{
    if ((fd = fopen(DESC, "a")) != NULL)
    {
        char *expmsg = "Expansion permutation E(R):", *keymsg = "subkey:", *xor = "E(R) xor K[i] :";
        display_permutation_tableM(E, 48, "Expansion permutation E.");
        // Expansion permutation E
        fprintf(fd, "\n\t\t\t%28s %50s\n", expmsg, representationIn48Bits(permutation));
        fprintf(fd, "\t\t\t%28s %50s\n", keymsg, representationIn48Bits(k));

        // The expansion is XORed with the round key k[i]
        fprintf(fd, "\t\t\t%28s %50s\n\n", xor, representationIn48Bits(E_xor_K));
    }
    else
    {
        printf("File not found (%s)", DESC);
        exit(0);
    }
    fclose(fd);
}

void display_s_box(unsigned char i, uint8_t in, uint8_t ou, int8_t S[][16])
{
    if ((fd = fopen(DESC, "a")) != NULL)
    {
        display_sbox_table(S, i);
        fprintf(fd, "\n");
        fprintf(fd, "\t\t\ts-box input[%d]:%7s\t s-box output[%d]: %5s\n", i, representationIn6Bits(in), i, representationIn4Bits(ou));
    }
    else
    {
        printf("File not found (%s)", DESC);
        exit(0);
    }
    fclose(fd);
}

void display_permutation_P(uint32_t  in, uint32_t  ou, int8_t P[])
{
    if ((fd = fopen(DESC, "a")) != NULL)
    {
        char *inmsg = "permutation_p_in:", *oumsg = "permutation_p_ou:";
        display_permutation_tableM(P, 32, "permutation P.");
        fprintf(fd, " \n\t\t\t%20s%33s \n\t\t\t%20s%33s\n\n", inmsg, representationIn32Bits(in), oumsg, representationIn32Bits(ou));
    }
    else
    {
        printf("File not found (%s)", DESC);
        exit(0);
    }
    fclose(fd);
}

void display_L_R(int8_t i, uint32_t  L, uint32_t  R)
{
    if ((fd = fopen(DESC, "a")) != NULL)
    {
        char *temp = " ";
        if (i < 16)
            fprintf(fd, "\n\n\t\t\t\t\tROUND %d \n\n", (i + 1));
        fprintf(fd, "\t\t\t%15sL[%d]:%33s\n\t\t\t%15sR[%d]:%33s", temp, i, representationIn32Bits(L), temp, i, representationIn32Bits((R)));
    }
    else
    {
        printf("File not found (%s)", DESC);
        exit(0);
    }
    fclose(fd);
}

void display_key_schedule_init(uint64_t key, uint64_t permuted_choice_1, uint32_t  C, uint32_t  D)
{
    if ((fd = fopen(DESC, "a")) != NULL)
    {
        fprintf(fd, "\t\t\tkey: %lx \n\n", key);
        fprintf(fd, "\t\t\tInitial key permutation PC-1: %lx \n", permuted_choice_1);
        fprintf(fd, "\t\t\tC[%02d]=%x\t D[%02d]=%x\n", 0, C, 0, D);
    }
    else
    {
        printf("File not found (%s)", DESC);
        exit(0);
    }
    fclose(fd);
}

void display_key_schedule_end(int8_t p, uint64_t key, uint32_t  C, uint32_t  D, int8_t r)
{
    if ((fd = fopen(DESC, "a")) != NULL)
    {
        fprintf(fd, "\t\t\tC[%02d]=%8x\t D[%02d]=%8x\t K[%02d]: %13lx \n", r, C, r, D, p, key);
    }
    else
    {
        printf("File not found (%s)", DESC);
        exit(0);
    }
    fclose(fd);
}

void display_sbox_table(int8_t S[][16], unsigned char nb)
{
    fprintf(fd, "\n\t\t\tS-box S%d", nb + 1);
    fprintf(fd, "\n\t\t\t");
    for (uint8_t i = 0; i < 4; i++)  // Correction ici
    {
        for (uint8_t x = 0; x < 16; x++)  // Correction ici
        {
            fprintf(fd, "%4d", S[i][x]);
        }

        fprintf(fd, "\n\t\t\t");
    }
}
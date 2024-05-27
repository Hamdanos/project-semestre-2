#include <stdio.h>
#include <stdlib.h>
#include "des.h"
#include "msg.h"
#include <stdint.h>

/* Permuted Choice 1 Table */
static int8_t PC1[] = {
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4};

/* Permuted Choice 2 Table */
static int8_t PC2[] = {
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32};

/* Initial permutation IP */
static int8_t IP[] = {
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7};

/*Final permutation IP_1*/
static int8_t IP_1[] = {
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25};

// Expansion permutation E
static int8_t E[] = {
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1};

// S-box S1
static int8_t S1[][16] = {
    {14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7},
    {0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8},
    {4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0},
    {15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13}};

// S-box S2
static int8_t S2[][16] = {
    {15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10},
    {3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5},
    {0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15},
    {13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9}};

// S-box S3
static int8_t S3[][16] = {
    {10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8},
    {13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1},
    {13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7},
    {1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12}};

// S-box S4
static int8_t S4[][16] = {
    {7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15},
    {13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9},
    {10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4},
    {3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14}};

// S-box S5
static int8_t S5[][16] = {
    {2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9},
    {14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6},
    {4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14},
    {11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3}};

// S-box S6
static int8_t S6[][16] = {
    {12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11},
    {10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8},
    {9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6},
    {4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13}};

// S-box S7
static int8_t S7[][16] = {
    {4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1},
    {13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6},
    {1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2},
    {6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12}};

// S-box S8
static int8_t S8[][16] = {
    {13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7},
    {1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2},
    {7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8},
    {2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11}};

// S-box
static int8_t (*S[])[16] = {S1, S2, S3, S4, S5, S6, S7, S8};

// The permutation P within the f-function
static int8_t P[] = {
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25};

uint64_t permutation(uint64_t key, int8_t final_size, int8_t start_size, int8_t tab_PC[]);
uint32_t  f_function(uint32_t  R, uint64_t k);
uint8_t*get_s_box_inputs(uint64_t E_xor_k);
uint8_t S_box(uint8_t input, int8_t (*S)[16]);

uint64_t permutation(uint64_t key, int8_t final_size, int8_t start_size, int8_t tab_PC[])
{
    uint64_t permuted = 0;

    for (int i = 0; i < final_size; i++)
    {
        permuted <<= 1;
        permuted |= (key >> (start_size - tab_PC[i])) & 0x0000000000000001;
    }

    return permuted;
}

uint32_t  f_function(uint32_t  R, uint64_t k)
{
    // Expansion permutation E
    uint64_t EP = permutation(R, 48, 32, E);

    // The expansion is XORed with the round key k[i]
    uint64_t E_xor_K = EP ^ k;

    display_f_function(EP, k, E_xor_K, E);

    // Split the E(R)xorK[i] in eight 6-bit blocks to get S-box inputs
    // and apply s_box to get s_box output
    uint8_t s_box_output[8];
    for (unsigned char i = 0; i < 8; i++)
    {
        s_box_output[i] = S_box(get_s_box_inputs(E_xor_K)[i], S[i]);

        display_s_box(i, get_s_box_inputs(E_xor_K)[i], s_box_output[i], S[i]);
    }

    // we join all the 8 s_box output of 4-bits to one
    uint32_t  permutation_p_in = 0;
    for (int i = 1; i < 9; i++)
    {
        permutation_p_in |= ((((uint32_t )s_box_output[i - 1]) & 0x0000000f) << (8 - i) * 4);
    }

    display_permutation_P(permutation_p_in, (uint32_t )permutation(permutation_p_in, 32, 32, P), P);

    return (uint32_t )permutation(permutation_p_in, 32, 32, P);
}

uint8_t*get_s_box_inputs(uint64_t E_xor_k)
{
    uint8_t*tab = malloc(sizeof(8));

    for (int i = 1; i < 9; i++)
    {
        tab[i - 1] = (E_xor_k >> (6 * (8 - i))) & 0x000000000000003f;
    }

    return tab;
}

uint8_t S_box(uint8_t input, int8_t (*S)[16]) {
    int8_t row, column;

    row = ((input >> 4) & 0x02 )| (input & 0x01);
    column = (input & 0x1e) >> 1;

    return S[row][column];
}

uint64_t *key_schedule(uint64_t key)
{
    uint64_t permuted_choice_1 = 0, permuted_choice_2 = 0;
    uint64_t *K = malloc(16 * sizeof(uint64_t));
    uint32_t  C[17], D[17];

    // Initial key permutation PC − 1
    permuted_choice_1 = permutation(key, 56, 64, PC1);

    // 56-bit key is split into two halves C[0] and D[0]
    C[0] = (permuted_choice_1 >> 28) & 0x000000000fffffff;
    D[0] = permuted_choice_1 & 0x000000000fffffff;

    display_key_schedule_init(key, permuted_choice_1, C[0], D[0]);

    for (int r = 1; r < 17; r++)
    {
        if (r == 1 || r == 2 || r == 9 || r == 16)
        {
            C[r] = ((C[r - 1] << 1) & 0x0fffffff )| ((C[r - 1] >> 27) & 0x0000001);
            D[r] = ((D[r - 1] << 1) & 0x0fffffff )| ((D[r - 1] >> 27) & 0x0000001);
        }
        else
        {
            C[r] = ((C[r - 1] << 2) & 0x0fffffff) | ((C[r - 1] >> 26) & 0x0000003);
            D[r] = ((D[r - 1] << 2) & 0x0fffffff) | ((D[r - 1] >> 26) & 0x0000003);
        }

        // we join the two halves C[0] and D[0]
        permuted_choice_2 = (((uint64_t)C[r]) << 28) | (uint64_t)D[r];

        // Key permutation PC − 2
        K[r - 1] = permutation(permuted_choice_2, 48, 56, PC2);
        display_key_schedule_end((r - 1), K[r - 1], C[r], D[r], r);
    }

    return K;
}

uint64_t encrypt(uint64_t x, uint64_t *k)
{
    // Initial permutation IP
    uint64_t ip = permutation(x, 64, 64, IP);

    // split the initial permutation into two halves L[0] and R[0]
    uint32_t  L[17], R[17];
    L[0] = (ip & 0xffffffff00000000) >> 32;
    R[0] = (ip & 0x00000000ffffffff);

    plaintext_init_msg(x, ip, L[0], R[0], IP, 1);

    // Expansion, substition and permutation
    for (int8_t i = 1; i < 17; i++)
    {
        L[i] = R[i - 1];
        R[i] = L[i - 1] ^ f_function(R[i - 1], k[i - 1]);
        display_L_R(i, L[i], R[i]);
    }

    // we join the two  L[16] and R[16]
    uint64_t F_LR = (((uint64_t)R[16]) << 32) | (uint64_t)L[16];

    display_permutation_table(IP_1, 64, "Final permutation IP-1");
    binary_expansion64(F_LR);
    binary_expansion64(permutation(F_LR, 64, 64, IP_1));

    return permutation(F_LR, 64, 64, IP_1);
}

uint64_t decrypt(uint64_t y, uint64_t *k)
{
    // Initial permutation IP
    uint64_t ip = permutation(y, 64, 64, IP);

    // split the initial permutation into two halves L[0] and R[0]
    uint32_t  L[17], R[17];
    L[0] = (ip & 0xffffffff00000000) >> 32;
    R[0] = (ip & 0x00000000ffffffff);

    plaintext_init_msg(y, ip, L[0], R[0], IP, 0);

    // Expansion, substition and permutation
    for (int8_t i = 1; i < 17; i++)
    {
        L[i] = R[i - 1];
        R[i] = L[i - 1] ^ f_function(R[i - 1], k[16 - i]);
        display_L_R(i, L[i], R[i]);
    }

    // we join the two  L[16] and R[16]
    uint64_t F_LR = (((uint64_t)R[16]) << 32) | (uint64_t)L[16];

    display_permutation_table(IP_1, 64, "Final permutation IP-1");
    binary_expansion64(F_LR);
    binary_expansion64(permutation(F_LR, 64, 64, IP_1));

    return permutation(F_LR, 64, 64, IP_1);
}
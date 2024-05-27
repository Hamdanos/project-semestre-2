
#include <stdlib.h>
#include <stdio.h>
#define DESC "desc.txt"
#include <stdint.h>

struct des_msg
{
    char *title;
    char *key_title;
};


void start_des();
void display_permutation_table(int8_t IP[], unsigned char size, char *t);
void display_des(uint64_t x, uint64_t *key, int8_t b);
void plaintext_init_msg(uint64_t x, uint64_t ip, uint32_t  L, uint32_t  R, int8_t IP[], int8_t b);
void display_f_function(uint64_t permutation, uint64_t k, uint64_t E_xor_K, int8_t E[]);
void display_s_box(unsigned char i, uint8_t in, uint8_t ou, int8_t S[][16]);
void display_permutation_P(uint32_t  in, uint32_t  ou, int8_t E[]);
void display_L_R(int8_t i, uint32_t  L, uint32_t  R);
void display_key_schedule_init(uint64_t key, uint64_t permuted_choice_1, uint32_t  C, uint32_t  D);
void display_key_schedule_end(int8_t p, uint64_t key, uint32_t  C, uint32_t  D, int8_t r);
void binary_expansion64(uint64_t x);
void display_sbox_table(int8_t S[][16], unsigned char nb);

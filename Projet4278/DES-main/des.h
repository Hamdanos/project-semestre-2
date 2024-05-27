#include <stdlib.h>
#include <stdint.h>

/* 
    Génère 16 clés de round de 48 bits chacune 
    à partir d'une clé initiale de 64 bits.
    @param uint64_t key : clé initiale
    @return un tableau constitué de 16 clés de round
*/
uint64_t *key_schedule(uint64_t key);
uint64_t encrypt(uint64_t x, uint64_t *key);
uint64_t decrypt(uint64_t y, uint64_t *key);
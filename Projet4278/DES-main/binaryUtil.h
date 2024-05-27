#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define LSB64 0x0000000000000001
#define LSB32 0x00000001
#define LSB48 0x000000000001
#define LSB6 0x01
#define LSB4 0x1

char *representationIn64Bits(uint64_t x);
char *representationIn32Bits(uint32_t  x);
char *representationIn48Bits(uint64_t x);
char *representationIn6Bits(uint8_t x);
char *representationIn4Bits(uint8_t x);
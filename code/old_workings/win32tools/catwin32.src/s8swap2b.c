#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <s8c32_prot.h>
void 
swap2b(unsigned short int *pic)
{
    unsigned char * puc;
    puc = (unsigned char *)pic;
    *pic = ((puc[0] << 8) & 0x0000ff00) + (puc[1] & 0x000000ff);
}

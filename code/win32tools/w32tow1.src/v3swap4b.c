#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void 
swap4b(unsigned int *pic)
{
    unsigned char * puc;
    puc = (unsigned char *)pic;
    *pic = (puc[0] << 24) + (puc[1] << 16) +
           (puc[2] << 8) + puc[3];
}

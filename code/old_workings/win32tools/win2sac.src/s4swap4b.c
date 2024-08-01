#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <s4win2sac.h>
void 
swap4b(unsigned int *pic)
{
    unsigned char * puc;
    puc = (unsigned char *)pic;
    *pic = ((puc[0] << 24) & 0xff000000) + ((puc[1] << 16) & 0xff0000) +
           ((puc[2] << 8) & 0xff00) + (puc[3] & 0xff);
}

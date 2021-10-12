#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void 
swap2b(unsigned short *pic)
{
#if 0
    unsigned char uc[2];
    memmove((char *)uc, (char *)pic, 2);
    *(pic+1)=uc[0];
    *(pic+0)=uc[1];
#else
    unsigned char * puc;
/* printf("*pic=[%d] (%s %d)\n", *pic, __FILE__, __LINE__); */
    puc = (unsigned char *)pic;
    *((unsigned short *)pic) = (puc[0] << 8) + puc[1];
/* printf("*pic=[%d] (%s %d)\n", *pic, __FILE__, __LINE__); */
#endif
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <y1wch_prot.h>
void
swap4b(unsigned int *pic)
{
#if 0
    unsigned char uc[4];
/* printf("111=[%d] (%s %d)\n", 111, __FILE__, __LINE__); */
    memmove((char *)uc, (char *)pic, 4);
    *(pic+3)=uc[0];
    *(pic+2)=uc[1];
    *(pic+1)=uc[2];
    *(pic+0)=uc[3];
#else
    unsigned char * puc;
/* printf("*pic=[%d] (%s %d)\n", *pic, __FILE__, __LINE__);  */
    puc = (unsigned char *)pic;
    *pic = (puc[0] << 24) + (puc[1] << 16) +
           (puc[2] << 8) + puc[3];
/* printf("*pic=[%d] (%s %d)\n", *pic, __FILE__, __LINE__);  */
#endif                        
}

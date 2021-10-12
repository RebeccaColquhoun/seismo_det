#include <stdlib.h> /** for CYGWIN by kjmatsu **/
#include <stdlib.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <y0wadd_prot.h>
void 
swap2b(unsigned short int *pic)
{
    unsigned char * puc;
    puc = (unsigned char *)pic;
    *pic = (puc[0] << 8) + puc[1];
}

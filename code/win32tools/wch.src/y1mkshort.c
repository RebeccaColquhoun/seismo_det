#include <y1mkutil_man.h>
#include <y1wch_prot.h>
unsigned short 
mkshort(unsigned char * ptr)                            /* 2バイトの文字列を ショート型
                                         * に変換 */
{
    unsigned char *ptr1;
    unsigned short a;
    ptr1 = (unsigned char *) &a;
    *ptr1++ = (*ptr++);
    *ptr1 = (*ptr);
    return a;
}

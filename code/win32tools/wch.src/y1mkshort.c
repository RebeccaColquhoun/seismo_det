#include <y1mkutil_man.h>
#include <y1wch_prot.h>
unsigned short 
mkshort(unsigned char * ptr)                            /* 2�Х��Ȥ�ʸ����� ���硼�ȷ�
                                         * ���Ѵ� */
{
    unsigned char *ptr1;
    unsigned short a;
    ptr1 = (unsigned char *) &a;
    *ptr1++ = (*ptr++);
    *ptr1 = (*ptr);
    return a;
}

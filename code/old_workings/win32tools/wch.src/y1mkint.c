#include <string.h>
#include <y1mkutil_man.h>
#include <y1wch_prot.h>
int mkint(unsigned char * ptr) /* 4�Х��Ȥ�ʸ������󥰷���
                                         * �Ѵ�  */
{
    unsigned int a;
    memmove(&a, ptr, 4);
    swap4b((unsigned int *)(&a));
    return a;
}

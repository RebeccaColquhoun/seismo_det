#include <string.h>
#include <y1wch_prot.h>
#include <y1mkutil_man.h>
int strcmp2(char   * s1, char   * s2)                         /* s1�� s2�� NULLʸ���ޤ���Ӥ�
                                         * �� */
{
    if (*s1 == '0' && *s2 == '9')
        return 1;
    else if (*s1 == '9' && *s2 == '0')
        return -1;
    else
        return strcmp(s1, s2);
}

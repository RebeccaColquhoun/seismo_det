#include <string.h>
#include <y0mkutil_man.h>
int strncmp2(char * s1, char * s2, int i)                     /* s1と s2を i文字数分比較する */
{
    if (*s1 == '0' && *s2 == '9')
        return 1;
    else if (*s1 == '9' && *s2 == '0')
        return -1;
    else
        return strncmp(s1, s2, i);
}

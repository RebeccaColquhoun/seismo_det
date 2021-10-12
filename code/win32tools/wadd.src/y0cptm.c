#include <y0wadd_prot.h>
int cptm(int * dst, int * src)                          /* srcを dstにコピーする */
{
    int     i;
    for (i = 0; i < 6; i++) {
        dst[i] = src[i];
    }
    return 0;
}

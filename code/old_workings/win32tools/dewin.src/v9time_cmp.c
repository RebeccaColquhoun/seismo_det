#include <v9dewin_ext.h>
int time_cmp(int * t1, int * t2, int i)
{
    int     cntr;
    int     iRet;
    cntr = 0;
    if (t1[cntr] < 70 && t2[cntr] > 70) {
        iRet = 1;
        goto ret;
    }
    if (t1[cntr] > 70 && t2[cntr] < 70) {
        iRet = -1;
        goto ret;
    }
    for (; cntr < i; cntr++) {
        if (t1[cntr] > t2[cntr]) {
            iRet = 1;
            goto ret;
        }
        if (t1[cntr] < t2[cntr]) {
            iRet = -1;
            goto ret;
        }
    }
    iRet = 0;
ret:;
    return iRet;
}

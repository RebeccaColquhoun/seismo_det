#include <time.h>
#include <y0wadd_prot.h>
int time_cmp(int * t1, int * t2, int i)                     /* t1と t2を i数分 比較する */
{
    int     cntr;
    cntr = 0;
    if (t1[cntr] < 70 && t2[cntr] > 70)
        return 1;
    if (t1[cntr] > 70 && t2[cntr] < 70)
        return -1;
    for (; cntr < i; cntr++) {
        if (t1[cntr] > t2[cntr])
            return 1;
        if (t1[cntr] < t2[cntr])
            return -1;
    }
    return 0;
}

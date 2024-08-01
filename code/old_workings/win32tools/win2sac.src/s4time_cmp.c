#include <s4win2sac.h>
int 
time_cmp(int *t1, int *t2)
{
    int     cntr;
    for (cntr = 0; cntr < 6; cntr++) {
        if (t1[cntr] > t2[cntr])
            return 1;
        if (t1[cntr] < t2[cntr])
            return -1;
    }
    return 0;
}

#include <y0wadd_n_man.h>
extern int giKbegin_main;
extern int giKbegin_sub;
extern int giKwin32_main;
extern int giKwin32_sub;
extern int giKwin32_both;
extern int giKwrite;
void bcd_dec(int *dest, char *sour)
{
    int     cntr;
    int     iCount;
    iCount = 6;
    if (giKwin32_both) iCount = 8;
    for (cntr = 0; cntr < iCount; cntr++) {
        dest[cntr] = ((sour[cntr] >> 4) & 0xf) * 10 + (sour[cntr] & 0xf);
    }
}

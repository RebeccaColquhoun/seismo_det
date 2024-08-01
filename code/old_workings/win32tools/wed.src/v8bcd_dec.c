#include <v8wed_ext.h>
int bcd_dec(int * dest, char * sour)
{
    int     cntr;
    for (cntr = 0; cntr < 6; cntr++) {
        dest[cntr] = ((sour[cntr] >> 4) & 0xf) * 10 + (sour[cntr] & 0xf);
    }
    return 0;
}

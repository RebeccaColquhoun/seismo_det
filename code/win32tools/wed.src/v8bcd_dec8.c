#include <v8wed_ext.h>
void bcd_dec8(int * dest, char * sour)
{
    int     cntr;
    for (cntr = 0; cntr < 6; cntr++) {
        dest[cntr] = ((sour[cntr+1] >> 4) & 0xf) * 10 + (sour[cntr+1] & 0xf);
    }
}

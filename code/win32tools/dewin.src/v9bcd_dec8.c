#include <v9dewin_ext.h>
void bcd_dec8(int    *dest, char   *sour)
{
    int     cntr;
    for (cntr = 0; cntr < 8; cntr++) {
        dest[cntr] = ((sour[cntr] >> 4) & 0xf) * 10 + (sour[cntr] & 0xf);
    }
}

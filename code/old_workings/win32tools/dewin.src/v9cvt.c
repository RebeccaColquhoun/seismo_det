#include <v9dewin_ext.h>
/* convert two's complement ch into uLAW format */
unsigned int
cvt(int ch)
{
    int     mask;
    if (ch < 0) {
        ch = -ch;
        mask = 0x7f;
    } else {
        mask = 0xff;
    }
    if (ch < 32) {
        ch = 0xF0 | (15 - (ch / 2));
    } else if (ch < 96) {
        ch = 0xE0 | (15 - (ch - 32) / 4);
    } else if (ch < 224) {
        ch = 0xD0 | (15 - (ch - 96) / 8);
    } else if (ch < 480) {
        ch = 0xC0 | (15 - (ch - 224) / 16);
    } else if (ch < 992) {
        ch = 0xB0 | (15 - (ch - 480) / 32);
    } else if (ch < 2016) {
        ch = 0xA0 | (15 - (ch - 992) / 64);
    } else if (ch < 4064) {
        ch = 0x90 | (15 - (ch - 2016) / 128);
    } else if (ch < 8160) {
        ch = 0x80 | (15 - (ch - 4064) / 256);
    } else {
        ch = 0x80;
    }
    return (mask & ch);
}

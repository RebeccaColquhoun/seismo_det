#include <v8BitOper_ext.h>
/* メモリ上の指定したビット数のデータを WinValue 型の値に変換 */
WinValue Win_GetValueB
        (WinData src, WinNumber start, WinNumber bits) {
    WinNumber rest = 8 - start;
    WinValue value = (*src & (0x80 >> start)) ? -1L : 0L;
    if (bits > rest) {
        value <<= rest;
        value |= *(src++) & (0xff >> start);
        bits -= rest;
        while (bits > 8) {
            value <<= 8;
            value |= *(src++);
            bits -= 8;
        }
        value <<= bits;
        value |= *src >> (8 - bits);
    } else {
        value <<= bits;
        value |= (*src & (0xff >> start)) >> (rest - bits);
    }
    return value;
}

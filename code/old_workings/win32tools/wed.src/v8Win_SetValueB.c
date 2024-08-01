#include <v8BitOper_ext.h>
/* WinValue 型の値をメモリ上の指定したビット位置に set */
void    Win_SetValueB
        (WinValue value, WinData dst, WinNumber start, WinNumber bits) {
    WinNumber rest = 8 - start;
    if (bits > rest) {
        WinNumber last = (start + bits) & 0x07;
        dst += (start + bits - 1) >> 3;
        if (last) {
            *dst &= 0xff >> last;
            *(dst--) |= (value << (8 - last)) & 0xff;
            value >>= last;
            bits -= last;
        }
        while (bits > 8) {
            *(dst--) = value & 0xff;
            value >>= 8;
            bits -= 8;
        }
        *dst &= 0xff << bits;
        *dst |= value & (0xff >> start);
    } else {
        *dst &= (0xff >> start) ^ (0xff << (rest - bits));
        *dst |= (value & ~(-1L << bits)) << (rest - bits);
    }
    return;
}

#include <v8BitOper_ext.h>
/* メモリ上の2バイトデータを、WinNumber 型の値に変換 */
WinNumber Win_GetNumber
        (WinData src) {
    WinNumber value;
    value = *(src++);
    value <<= 8;
    value |= *(src);
    return value;
}

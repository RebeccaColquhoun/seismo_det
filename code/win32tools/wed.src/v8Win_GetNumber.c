#include <v8BitOper_ext.h>
/* ������2�Х��ȥǡ�����WinNumber �����ͤ��Ѵ� */
WinNumber Win_GetNumber
        (WinData src) {
    WinNumber value;
    value = *(src++);
    value <<= 8;
    value |= *(src);
    return value;
}

#include <v8BitOper_ext.h>
/* WinValue �����ͤ�����λ��ꤷ���Х��Ȱ��֤� set */
void    Win_SetValue
        (WinValue value, WinData dst, WinNumber leng) {
    dst += leng - 1;
    while (leng--) {
        *(dst--) = value & 0xff;
        value >>= 8;
    }
    return;
}

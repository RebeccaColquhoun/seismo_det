#include <v8mkutil_man.h>
#include <v8winlib.h>
/* �����ͥ�֥�å����顢Win �ΥС���������� */
WinNumber WinGetVersion
        (WinData src) {
    return (src[2] & 0x80) ? 2 : 1;
}

#include <v8mkutil_man.h>
#include <v8winlib.h>
/* �����ͥ�֥�å��Υ���������� */
WinNumber WinGetChSize
        (WinData src) {
    return WinGetChParam(src).blk_size;
}

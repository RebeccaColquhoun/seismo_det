#include <v8Win2Pack_man.h>
/* 1��ʬ�� win2 �ǡ����� win ���Ѵ� */
WinSize Win2UpkSec
        (WinData src, WinSize leng, WinData dst) {
    return _PkSecSub(src, leng, dst, Win2UpkCh);
}

#include <v8Win2Pack_man.h>
/* 1��ʬ�� win2 �ǡ����� win ���Ѵ� (�Ѵ���Υ������׻��Τ�) */
WinSize Win2UpkSecSize
        (WinData src, WinSize leng) {
    return _PkSecSub(src, leng, NULL, Win2UpkCh);
}

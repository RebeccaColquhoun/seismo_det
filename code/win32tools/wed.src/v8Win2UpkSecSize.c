#include <v8Win2Pack_man.h>
/* 1秒分の win2 データを win に変換 (変換後のサイズ計算のみ) */
WinSize Win2UpkSecSize
        (WinData src, WinSize leng) {
    return _PkSecSub(src, leng, NULL, Win2UpkCh);
}

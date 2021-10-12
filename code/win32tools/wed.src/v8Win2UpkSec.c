#include <v8Win2Pack_man.h>
/* 1秒分の win2 データを win に変換 */
WinSize Win2UpkSec
        (WinData src, WinSize leng, WinData dst) {
    return _PkSecSub(src, leng, dst, Win2UpkCh);
}

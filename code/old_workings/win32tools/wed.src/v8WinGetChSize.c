#include <v8mkutil_man.h>
#include <v8winlib.h>
/* チャンネルブロックのサイズを取得 */
WinNumber WinGetChSize
        (WinData src) {
    return WinGetChParam(src).blk_size;
}

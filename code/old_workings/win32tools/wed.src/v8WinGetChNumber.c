#include <v8mkutil_man.h>
#include <v8winlib.h>
/* チャンネルブロックから、チャンネル番号を取得 */
WinNumber WinGetChNumber
        (WinData src) {
    return Win_GetNumber(src);
}

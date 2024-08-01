#include <v8mkutil_man.h>
#include <v8winlib.h>
/* チャンネルブロックから、Win のバージョンを取得 */
WinNumber WinGetVersion
        (WinData src) {
    return (src[2] & 0x80) ? 2 : 1;
}

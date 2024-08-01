#ifndef V8GETPARAM_MAN_HHHH
#define V8GETPARAM_MAN_HHHH
#define _GETPARAM_C_

#include <stdlib.h>
#include <v8winlib.h>

/* プロトタイプ宣言 */
extern WinNumber _GetChParamList
        (WinData, WinSize, ChParamList *, ChParam(*) (WinData));
extern WinData _SearchChNumber
        (WinData, WinSize, WinNumber, ChParam(*) (WinData));
extern WinNumber _SearchChList
        (WinData, WinSize, ChParamList, WinNumber, ChParam(*) ());
#endif

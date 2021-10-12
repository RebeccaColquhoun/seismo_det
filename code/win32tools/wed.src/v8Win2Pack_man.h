#ifndef V8WIN2PACK_MAN_HHHH
#define V8WIN2PACK_MAN_HHHH

#define _WIN2PACK_C_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <v8winlib.h>

/* サンプルサイズ、サンプリングレートの読み込み */
#define GET_SR(ptr, smpl_size, smpl_rate)           \
{                                                   \
  smpl_size = *(ptr + 2);                           \
  smpl_size <<= 8;                                  \
  smpl_size |= *(ptr + 3);                          \
  /* Win format V2 */                               \
  if (smpl_size & 0x8000){                          \
    smpl_rate = smpl_size & 0x03ff;                 \
    smpl_size = ((smpl_size >> 10) & 0x3f) - 0x1f;  \
  }                                                 \
  /* Win format V1 */                               \
  else {                                            \
    smpl_rate = smpl_size & 0x0fff;                 \
    smpl_size = (smpl_size >> 12) & 0x0f;           \
    if (smpl_size > 4) return 0;                    \
    smpl_size <<= 3;                                \
    if (smpl_size == 0) smpl_size = 4;              \
  }                                                 \
  if (smpl_rate == 0) return 0;                     \
}

/* プロトタイプ宣言 */
extern WinSize _PkSecSub
        (WinData, WinSize, WinData, WinNumber(*) (WinData, WinData));
#endif

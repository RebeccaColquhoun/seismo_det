#ifndef C20_TYPE___H
#define C20_TYPE___H

#include <sys/types.h>
#ifdef MINGW
#include <stdio.h>
#include <fcntl.h>
#include <io.h>
#else
#include <unistd.h>
#endif

typedef int (*COMP) (const void *, const void *);

typedef struct __C20_HEADER {
    unsigned char ucStart[8];    /** サンプリング開始年月日時分秒＋０．０１秒 **/
    int           iNframe;       /** フレーム時間長（０．１秒単位） **/
    unsigned short int uhChanno0; /** 組織ID&組織内網ID **/
    unsigned short int uhChanno; /** チャンネル番号 **/
#ifdef MINGW
    int           tOffset;       /** ファイルのオフセット位置 **/
#else
    off_t         tOffset;       /** ファイルのオフセット位置 **/
#endif
    int           iByte;         /** バイト数 **/
}       C32_HEADER;

typedef struct __WIDECHAN {
    unsigned short int uhChan0;  /** 組織ID&組織内網 **/
    unsigned short int uhChan;   /** チャンネル番号 **/
}       WIDECHAN;

#endif  /** C20_TYPE___H **/

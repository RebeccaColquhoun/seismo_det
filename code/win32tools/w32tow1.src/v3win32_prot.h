#ifndef APE_PROT___H
#define APE_PROT___H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h>
#include <fcntl.h>

#ifdef DOS
#else
#include <unistd.h>
#endif

#include <v3win32_type.h>
#include <v3win32_define.h>

extern int
winget_chnl(
    unsigned char *pucPtr,              /* ( I ) チャンネルデータ （チ
                                         * ャンネル番号から） */
    unsigned short *puhSys_ch,          /* ( O ) チャンネル番号 */
    int *piOffsize,                     /* ( O ) サンプルサイズ(0---4) */
    int *piNsampno,                     /* ( O ) サンプリング数 */
    int *piAllbyte                      /* ( O ) 全バイト数 * */
);

extern void usage(void);

extern int
read_write(
    FILE * psFile_in,
    FILE * psFile_out
);

extern int maxalloc(
    void **ppvPtr,    /** (I/O) ポインタ **/
    int   iAllbyte,   /** ( I ) allocするバイト数 **/
    int  *piMaxbyte   /** ( I ) 現在のバイト数 **/
);

extern void w32las_(
    char * pcFilenow,        /** ( O ) 現在のファイル名 **/
    char * pcLast3,          /** ( O ) 最後から３つ目のデータ名 **/
    int  * piRet             /** ( O ) リターンコード(= 0 正常、!= 0 異常終了) **/
);

extern void w32nxt_(
    char * pcFilenow,        /** ( I ) 現在のデータファイル名 **/
    char * pcFileend,        /** ( I ) エンド時刻データファイル名 **/
    char * pcFilenext,       /** ( O ) 次のデータファイル名 **/
    int  * piRet             /** ( O ) リターンコード(= 0 正常、!= 0 異常終了) **/
);

extern int w32cmpdata(
    WIN32_DATA * pstData1,
    WIN32_DATA * pstData2
);

extern void w32dir_(
    char * pcFilename,       /** ( I ) ファイル名(２２文字の日付ファイル名) **/
    char * pcFiledir,        /** ( I ) ディレクトリー名 **/
    int * piRet
);
extern void thrini_(
    int * piPid1,  /** ( O ) プロセスＩＤ（END待ち） **/
    int * piPid2   /** ( O ) プロセスＩＤ（親プロセス監視用） **/
);
extern void setglb_(
    char * pcEnv           /** ( I ) データの存在するディレクトリー **/
);
extern void setgl2_(
    char * pcEnv           /** ( I ) データの存在するディレクトリー **/
);
extern void thrwat_(
    int * piPid,
    int * piIstat,
    int * piRet
);
extern void bytrev_(unsigned char * puc1, int * piByte);
extern void lastdt_(
    char * pcLast3,          /** ( O ) 最後から３つ目のデータ名 **/
    int  * piRet             /** ( O ) リターンコード(= 0 正常、!= 0 異常終了) **/
);
extern void bitmov_(
    unsigned char * pucTo,       /** ( O ) 移動先のバイトエリア **/
    int           * piBitadrTo,  /** ( I ) pucToの先頭からのビットアドレス(０または４の倍数) **/
    unsigned char * pucFr,       /** ( I ) 移動元のバイトエリア **/
    int           * piBitadrFr,  /** ( I ) pucFrの先頭からのビットアドレス(０または４の倍数) **/
    int           * piBitnum     /** ( I ) 移動するビット数(４の倍数) **/
);
extern void w32ums_(
    int  * piMode,   /** ( I ) 設定するマスク値 **/
    int  * piOld     /** ( O ) それまでのマスク値 **/
);
extern void w32mkd_(
    char * pcPath,
    int  * piMode
);
extern int w32cmp( char * pcFile1, char * pcFile2);
extern void bit4mv_(
    unsigned char * pucTo,      /** ( O ) char of To **/
    int           * piBitadrTo,  /** ( I ) pucToのビットアドレス(０または４の倍数) **/
    unsigned char * pucFr,      /** ( I ) char of From **/
    int           * piBitadrFr   /** ( I ) pucFrのビットアドレス(０または４の倍数) **/
);
extern int date32_(
    char * pcDate1,
    char * pcDate2,
    size_t  * piNum
);
extern void w32upp_(
    char * pcFilestart,      /** ( I ) 現在のデータファイル名 **/
    char * pcFileend,        /** ( I ) エンド時刻データファイル名 **/
    char * pcFilenext,       /** ( O ) 次のデータファイル名 **/
    int  * piRet             /** ( O ) リターンコード(= 0 正常、!= 0 異常終了) **/
);
extern void w32nxt_(
    char * pcFilenow,        /** ( I ) 現在のデータファイル名 **/
    char * pcFileend,        /** ( I ) エンド時刻データファイル名 **/
    char * pcFilenext,       /** ( O ) 次のデータファイル名 **/
    int  * piRet             /** ( O ) リターンコード(= 0 正常、!= 0 異常終了) **/
);
extern void w32fnm_(
    char * pcFilenow,        /** ( I ) 現在のデータファイル名 **/
    int  * piKbegin,         /** ( I ) 次のデータファイル名の求め方
                              **       1:無条件に最初のデータファイルを取り出す
                              **       2:pcFilenowより大きい又は等しいもの
                              **       3:pcFilenowより小さい又は等しいもの
                              **       4:無条件に最後のデータファイルを取り出す
                              **       その他:pcFilenowの次のもの
                              **/
    char * pcFilenext,       /** ( O ) データファイル名 **/
    int * piRet              /** ( O ) リターンコード(= 0 正常、!= 0 異常終了) **/
);
extern void win32read_(
    int * piStart,           /** ( I ) 初期オープンか(1:YES, 0:NO) **/
    char * pcFilestart,      /** ( I ) 初期オープンするファイル名(１１文字の日付ファイル名) **/
    char * pcFileend,        /** ( I ) 最後のファイル名(１１文字の日付ファイル名) **/
    int  * piRet             /** ( O ) リターンコード(0:正常、1:データ終了、999:異常終了) **/
);
extern void w32dwn_(
    char * pcFilestart,      /** ( I ) 現在のデータファイル名 **/
    char * pcFileend,        /** ( I ) エンド時刻データファイル名 **/
    char * pcFilenext,       /** ( O ) 次のデータファイル名 **/
    int  * piRet             /** ( O ) リターンコード(= 0 正常、!= 0 異常終了) **/

);
extern void w32ls1_(
    char * pcFilenow,        /** ( I ) 現在のデータファイル名 **/
    int * piRet              /** ( O ) リターンコード(= 0 正常、!= 0 異常終了) **/
);

extern void swap4b(unsigned int *pic);
extern void swap2b(unsigned short int *pic);
extern void bit4mv_(
    unsigned char * pucTo,        /** ( O ) char of To **/
    int           * piBitadrTo,   /** ( I ) pucToのビットアドレス(０または４の倍数) **/
    unsigned char * pucFr,        /** ( I ) char of From **/
    int           * piBitadrFr    /** ( I ) pucFrのビットアドレス(０または４の倍数) **/
);


#endif

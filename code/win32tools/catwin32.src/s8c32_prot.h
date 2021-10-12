#ifndef C20_PROT__HHH
#define C20_PROT__HHH

#include <s8c32_type.h>

extern int c32dataread_write(
    int           iKbeginfile,     /** ( I ) 最初のファイルか **/
    char        * pcFilename_out,  /** ( I ) 読み込むＷＩＮ３２データファイル名 **/
    char        * pcFilename_in,   /** ( I ) 読み込むＷＩＮ３２データファイル名 **/
    int         *piHandle_out,
    int         *piHandle_in
);

extern void c32realloc(
    C32_HEADER **pptHeader,    /** (I/O) ヘッダーのポインター **/
    int          iNheader      /** ( I ) 確保するヘッダーの個数 **/
);

extern void c32dataread(
    unsigned char   ucTop[4],      /** (I/O) ファイルの先頭４バイト **/
    C32_HEADER ** pptC32header,    /** (I/O) ヘッダー部分のポインター **/
    int         * piNchannel,       /** (I/O) 全チャンネルの個数(ヘッダーの個数) **/
    int           iHandle_temp,    /** ( I ) テンポラリーファイルのハンドル **/
#ifdef MINGW
    int         * ptCurpos,        /** (I/O) テンポラリーファイルカレントポジション **/
#else
    off_t       * ptCurpos,        /** (I/O) テンポラリーファイルカレントポジション **/
#endif
    char        * pcFilename       /** ( I ) 読み込むＷＩＮ３２データファイル名 **/
);

extern void ftime_(int * iTime);

extern void bytrev_(unsigned char * puc1, int * piByte);

extern void bitmov_(
    unsigned char * pucTo,       /** ( O ) 移動先のバイトエリア **/
    int           * piBitadrTo,  /** ( I ) pucToの先頭からのビットアドレス(０または４の倍数) **/
    unsigned char * pucFr,       /** ( I ) 移動元のバイトエリア **/
    int           * piBitadrFr,  /** ( I ) pucFrの先頭からのビットアドレス(０または４の倍数) **/
    int           * piBitnum     /** ( I ) 移動するビット数(４の倍数) **/
);

extern void bit4mv_(
    unsigned char * pucTo,      /** ( O ) char of To **/
    int           * piBitadrTo,  /** ( I ) pucToのビットアドレス(０または４の倍数) **/
    unsigned char * pucFr,      /** ( I ) char of From **/
    int           * piBitadrFr   /** ( I ) pucFrのビットアドレス(０または４の倍数) **/
);

extern void c32datawrite(
    unsigned char ucTop[4],        /** (I/O) ファイルの先頭４バイト **/
    C32_HEADER ** pptC32header,    /** (I/O) ヘッダー部分のポインター **/
    int         * piNchannel,      /** (I/O) 全チャンネルの個数(ヘッダーの個数) **/
    int           iHandle_temp,    /** ( I ) テンポラリーファイルのハンドル **/
    char        * pcFilename,      /** ( I ) 出力ＷＩＮ３２データファイル名 **/
    WIDECHAN    *puiAll_channel,   /** ( I ) 全データに存在するチャンネル
                                         **       同じものは、はぶいてある **/
    int iNall_channel                   /** ( I ) 全データに存在するチャンネルの総数
                                         **       puiAll_channelの個数 **/

);

extern void c32datasort(
    C32_HEADER ** pptC32header,            /** (I/O) ヘッダー部分のポインター **/
    int         * piNchannel,              /** (I/O) 全チャンネルヘッダーの個数 **/
    WIDECHAN **ppuiAll_channel,            /** ( O ) 全データに存在するチャンネル
                                            **       同じものは、はぶいてある **/
    int *piNall_channel                    /** ( O ) 全データに存在するチャンネルの総数
                                            **       **ppuiAll_channelの個数 **/
);
extern int c32cmp1(
    C32_HEADER * pstData1,
    C32_HEADER * pstData2
);

extern void c32usage(void);
extern int maxalloc(
    void **ppvPtr,    /** (I/O) ポインタ **/
    int   iAllbyte,   /** ( I ) allocするバイト数 **/
    int  *piMaxbyte   /** ( I ) 現在のバイト数 **/
);
extern int c32cmp2(
    WIDECHAN * pstData1,
    WIDECHAN * pstData2
);
extern int
winget_chnl(
    unsigned char *pucPtr,              /* ( I ) チャンネルデータ （チ
                                         * ャンネル番号から） */
    unsigned short *puhSys_ch,          /* ( O ) チャンネル番号 */
    int *piOffsize,                     /* ( O ) サンプルサイズ(0---4) */
    int *piNsampno,                     /* ( O ) サンプリング数 */
    int *piAllbyte                      /* ( O ) 全バイト数 * */
);
extern void swap4b(unsigned int *pic);
extern void swap2b(unsigned short int *pic);


#endif  /** C20_PROT__HHH **/

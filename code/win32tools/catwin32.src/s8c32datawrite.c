#ifdef MINGW
/* #undef _INC_FCNTL */
#include <fcntl.h>
#if 0
#define O_RDONLY       0x0000  /* open for reading only */
#define O_WRONLY       0x0001  /* open for writing only */
#define O_RDWR         0x0002  /* open for reading and writing */
#define O_APPEND       0x0008  /* writes done at eof */
#define O_CREAT        0x0100  /* create and open file */
#define O_TRUNC        0x0200  /* open and truncate */
#define O_EXCL         0x0400  /* open only if file doesn't already exist */
#define O_TEXT         0x4000  /* file mode is text (translated) */
#define O_BINARY       0x8000  /* file mode is binary (untranslated) */
#endif
#else
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#endif
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <s8c32_type.h>
#include <s8c32_prot.h>
#define MAXBYTE 5000000
void c32datawrite(
    unsigned char ucTop[4],        /** (I/O) ファイルの先頭４バイト **/
    C32_HEADER ** pptC32header,    /** (I/O) ヘッダー部分のポインター **/
    int         * piNchannel,      /** (I/O) 全チャンネルの個数(ヘッダーの個数) **/
    int           iHandle_temp,    /** ( I ) テンポラリーファイルのハンドル **/
    char        * pcFilename,      /** ( I ) 出力ＷＩＮ３２データファイル名 **/
    WIDECHAN *puiAll_channel,      /** ( I ) 全データに存在するチャンネル
                                         **       同じものは、はぶいてある **/
    int iNall_channel                   /** ( I ) 全データに存在するチャンネルの総数
                                         **       puiAll_channelの個数 **/ 
)
{
    unsigned char * pc;
    unsigned short int uhWork;
    unsigned short int * puiExist_channel;
    unsigned char ucWork[10];
    int iSec_count;
    int iErr;
    int iHandle;
    int ia;
    int ib;
    int ic;
    int iNexist_channel = 0;
    int iNstart = 0;
    int iNsec_chan = 0;
    size_t iSize;
    size_t iSsize;
#ifdef MINGW
    int  iOffset;
#else
    off_t iOffset;
#endif
    int iChannelbyte;
    int iNframe;
/*    unsigned char ucDat[MAXBYTE]; */
    static unsigned char * pucDat = NULL;
    unsigned char ucStart[8];
    int kkkkkk;
#ifdef MINGW
    int result;
#endif
fprintf(stderr, "The output file name = %s\n", pcFilename);
    kkkkkk = 0;
    iErr = 0;               /** エラーコードゼロセット **/
    /** 出力ＷＩＮ３２データファイルをオープン **/
    if (pcFilename[0] == '\0') {  /** ＮＵＬＬの場合？ **/
        iHandle = 1;              /** 標準出力にする **/
#ifdef MINGW
       /* "stdout" をバイナリ モードに設定します。 */
        result = _setmode( _fileno( stdout ), _O_BINARY );
        if( result == -1 ) {
            fprintf(stderr, "***** ERROR ***** The mode does not set.(%s %d)\n",
                    __FILE__, __LINE__);
           exit(0);
        }
#endif
    } else {
#ifdef MINGW
        iHandle = open(pcFilename, O_WRONLY | O_CREAT | O_TRUNC | O_BINARY,0666 );
#else
        iHandle = open(pcFilename, O_WRONLY | O_CREAT | O_TRUNC ,0666 );
#endif
                                  /** 指定ファイルをオープン **/
        if ( iHandle == -1 ) {
            fprintf (stderr, "***** ERROR ***** File open error.(%s)(c32datawrite)\n",
                             pcFilename ) ;
            iErr = 1;
        }
    }
    /** 最初の１秒間に存在したチャンネル **/
    puiExist_channel = (unsigned short int *)calloc((size_t)iNall_channel,
                                                     sizeof(unsigned short int));
    if (puiExist_channel == NULL) {
        printf("***** ERROR ***** Memory alloc error.(c32datawrite)\n");
        exit (0);
    }
    /** トップ部分を書き込む **/
    if (iErr == 0) {
        iSize = write(iHandle, ucTop, (size_t)4);
        if (iSize != 4) {
            fprintf(stderr, "***** ERROR ***** File write error.(c32datawrite)\n");
            iErr = 1;
        }
    }
    ucStart[0] = 255;  /** 前回書き込みをしたサンプリング開始年月日秒 **/
    if (iErr == 0) {
        iSec_count = 0;      /** 書き込みをした、秒の数のカウント **/
        for (ia=0; ia<*piNchannel; ia++) {  /** 総チャンネル数でループ **/
            for (ib=0; ib<8; ib++) {
                if (ucStart[ib] != (*pptC32header+ia)->ucStart[ib]) break;
            }
            if (ib < 8) {  /** サンプリング開始年月日秒が前回と異なる時 **/
                iSec_count++;
                memmove(ucStart, (*pptC32header+ia)->ucStart, 8);
                iChannelbyte = 0;  /** チャンネルブロックトータルバイト数ゼロセット **/
                iNexist_channel = 0;
                for (ib=ia; ib<*piNchannel; ib++) {
                    if ((*pptC32header+ia)->ucStart[6] != (*pptC32header+ib)->ucStart[6] ||
                        (*pptC32header+ia)->ucStart[7] != (*pptC32header+ib)->ucStart[7] ||
                        (*pptC32header+ia)->ucStart[5] != (*pptC32header+ib)->ucStart[5] ||
                        (*pptC32header+ia)->ucStart[4] != (*pptC32header+ib)->ucStart[4] ||
                        (*pptC32header+ia)->ucStart[3] != (*pptC32header+ib)->ucStart[3] ||
                        (*pptC32header+ia)->ucStart[2] != (*pptC32header+ib)->ucStart[2] ||
                        (*pptC32header+ia)->ucStart[1] != (*pptC32header+ib)->ucStart[1] ||
                        (*pptC32header+ia)->ucStart[0] != (*pptC32header+ib)->ucStart[0]) break;
                    iChannelbyte += ((*pptC32header+ib)->iByte);
                    if (iSec_count == -1) {  /** これは、実行されない **/
                        puiExist_channel[iNexist_channel] = (*pptC32header+ib)->uhChanno;
                        iNexist_channel++;
                    }
                }
                if (iSec_count == -1) {  /** これは、実行されない **/
                    qsort((void *)(puiExist_channel), (size_t)iNexist_channel,
                                sizeof(unsigned short int), (COMP) c32cmp2);
                    for (ib=0; ib<iNexist_channel; ib++) {
                    }
                }
                /** サンプリング開始年月日時分秒を書き込む **/
                iSize = write(iHandle, (*pptC32header+ia)->ucStart, (size_t)8);
                if (iSize != 8) {
                    fprintf(stderr, "***** ERROR ***** File write error.(c32datawrite)\n");
                    iErr = 1;
                    break;
                }
                /** フレーム時間長を書き込む **/
                iNframe = (*pptC32header+ia)->iNframe;
/*                 bytrev_((unsigned char *)&iNframe, (int *)(&i04)); */
                swap4b((unsigned int *)&iNframe);
                iSize = write(iHandle, &iNframe, (size_t)4);
                if (iSize != 4) {
                    fprintf(stderr, "***** ERROR ***** File write error.(c32datawrite)\n");
                    iErr = 1;
                    break;
                }
                /** データブロック長を書き込む **/
                if (iSec_count == -1) { /** 最初の１秒の場合は、データブロック長を再計算 **/  /** これは、実行されない **/
                      iChannelbyte += 10*(iNall_channel - iNexist_channel);
                                  /** 10バイトとは組織ID 組織内網ID チャンネル番号
                                   **          サンプルサイズ サンプル数
                                   **          サンプル１データ の合計バイト**/
                }
/*                 bytrev_((unsigned char *)&iChannelbyte, (int *)(&i04)); */
                swap4b((unsigned int *)&iChannelbyte);
                iSize = write(iHandle, &iChannelbyte, (size_t)4);                   
                if (iSize != 4) {
                    fprintf(stderr, "***** ERROR ***** File write error.(c32datawrite)\n");
                    iErr = 1;
                    break;
                }
                iNsec_chan = 0;
                iNstart = 0;
            }
            if (iSec_count == -1) { /** これは、実行されない **/
                iNsec_chan++;  /** 最初の１秒間の何個目のデータか **/
                /** 元のチャンネルデータを読み込む **/
#ifdef MINGW
                iOffset = lseek(iHandle_temp, (int)(*pptC32header+ia)->tOffset, SEEK_SET);
                if (iOffset != (int)(*pptC32header+ia)->tOffset) {
                    fprintf(stderr, "***** ERROR ***** File seek error.(c32datawrite)\n");
                    iErr = 1;
                    break;
                }
#else
                iOffset = lseek(iHandle_temp, (off_t)(*pptC32header+ia)->tOffset, SEEK_SET);
                if (iOffset != (off_t)(*pptC32header+ia)->tOffset) {
                    fprintf(stderr, "***** ERROR ***** File seek error.(c32datawrite)\n");
                    iErr = 1;
                    break;
                }
#endif
                if ((*pptC32header+ia)->iByte >= MAXBYTE) {
                    fprintf(stderr, "***** ERROR ***** The data block length is over maximum. (%d)(%s %d)\n",
                            MAXBYTE, __FILE__, __LINE__);
                    exit (0);
                }
                if (pucDat != NULL) free(pucDat);
                pucDat = malloc((size_t)((*pptC32header+ia)->iByte));
                if (pucDat == NULL) {
                    fprintf(stderr, "***** ERROR ***** Memory alloc error.(%s %d)\n",
                            __FILE__, __LINE__);
                    exit(0);
                }
                iSsize = read(iHandle_temp, pucDat, (size_t)((*pptC32header+ia)->iByte));
                if (iSsize != (size_t)(*pptC32header+ia)->iByte) {
                    fprintf(stderr, "***** ERROR ***** File read error.(c32datawrite)\n");
                    iErr = 1;
                    break;
                }
                for (ib=0; ib<iNall_channel; ib++) {
                    if ((puiAll_channel+ib)->uhChan0 == (*pptC32header+ia)->uhChanno &&
                        (puiAll_channel+ib)->uhChan == (*pptC32header+ia)->uhChanno) break;
                }
                memmove(ucWork, pucDat, 2);  /** 組織ID＆組織内網ID **/
                memmove(&uhWork, pucDat, 2);  /** 組織ID＆組織内網ID **/
                if (iNstart < ib) {
                    for (ic=iNstart; ic<=ib-1; ic++) {
                        /** チャンネルのダミーデータを書き込む **/
                        memmove(&ucWork[0], &((puiAll_channel+ic)->uhChan0), 2);
                                                                      /** 組織ID＆組織内網ID **/
                        memmove(&ucWork[2], &((puiAll_channel+ic)->uhChan), 2);
                                                                      /** チャンネル番号 **/
                        ucWork[4] = 0;
                        ucWork[5] = 0;
                        ucWork[6] = 0;
                        ucWork[7] = 0;
                        ucWork[8] = 0;
                        ucWork[9] = 0;
                        iSize = write(iHandle, ucWork, (size_t)10);
                        if (iSize != (size_t)10) {
                            fprintf(stderr, "***** ERROR ***** File write error.(c32datawrite)\n");
                            iErr = 1;
                            break;
                        }
                    }
                }
                iNstart = ib+1;
                iSize = write(iHandle, pucDat, (size_t)(*pptC32header+ia)->iByte);
                if (iSize != (size_t)(*pptC32header+ia)->iByte) {
                    fprintf(stderr, "***** ERROR ***** File write error.(c32datawrite)\n");
                    iErr = 1;
                    break;
                }
                if (iNsec_chan == iNexist_channel) {
                                    /** 最後のチャンネルブロックデータだった時 **/
                    if (iNstart < iNall_channel) {
                        for (ic=iNstart; ic<=iNall_channel-1; ic++) {
                            /** チャンネルのダミーデータを書き込む **/
                            memmove(&ucWork[0], &((puiAll_channel+ic)->uhChan0), 2);
                                                                /** 組織ID＆組織内網ID **/   
                            memmove(&ucWork[2], &((puiAll_channel+ic)->uhChan), 2);
                                                                /** チャンネル番号 **/   
                            ucWork[4] = 0;
                            ucWork[5] = 0;
                            ucWork[6] = 0;
                            ucWork[7] = 0;
                            ucWork[8] = 0;
                            ucWork[9] = 0;
                            iSize = write(iHandle, ucWork, (size_t)10);                        
                            if (iSize != (size_t)10) {                        
                                fprintf(stderr,
                                       "***** ERROR ***** File write error.(c32datawrite)\n");
                                iErr = 1;
                                break;
                            }
                        }
                    }
                }
            } else {
                /** 元のチャンネルデータを読み込む **/
#ifdef MINGW
                iOffset = lseek(iHandle_temp, (int)(*pptC32header+ia)->tOffset, SEEK_SET);
                if (iOffset != (int)(*pptC32header+ia)->tOffset) {
                    fprintf(stderr, "***** ERROR ***** File seek error.(c32datawrite)\n");
                    iErr = 1;
                    break;
                }
#else
                iOffset = lseek(iHandle_temp, (off_t)(*pptC32header+ia)->tOffset, SEEK_SET);
                if (iOffset != (off_t)(*pptC32header+ia)->tOffset) {
                    fprintf(stderr, "***** ERROR ***** File seek error.(c32datawrite)\n");
                    iErr = 1;
                    break;
                }
#endif
                if ((*pptC32header+ia)->iByte >= MAXBYTE) {
                    fprintf(stderr, "***** ERROR ***** The data block length is over maximum. (%d)(%s %d)\n",
                            MAXBYTE, __FILE__, __LINE__);
                    exit (0);
                }
                if (pucDat != NULL) free(pucDat);
                pucDat = malloc((size_t)((*pptC32header+ia)->iByte));
                if (pucDat == NULL) {
                    fprintf(stderr, "***** ERROR ***** Memory alloc error.(%s %d)\n",
                            __FILE__, __LINE__);
                    exit(0);
                }
                iSsize = read(iHandle_temp, pucDat, (size_t)(*pptC32header+ia)->iByte);
                if (iSsize != (size_t)(*pptC32header+ia)->iByte) {
                    fprintf(stderr, "***** ERROR ***** File read error.(c32datawrite)\n"); 
                    iErr = 1;
                    break;
                }
                pc = (unsigned char *)(&uhWork);
                memmove(&uhWork, &pucDat[0], 2);
                uhWork = pc[1] + (((int) pc[0]) << 8);
                memmove(&uhWork, &pucDat[2], 2);
                uhWork = pc[1] + (((int) pc[0]) << 8);
                iSize = write(iHandle, pucDat, (size_t)(*pptC32header+ia)->iByte);
                if (iSize != (size_t)(*pptC32header+ia)->iByte) {
                    fprintf(stderr, "***** ERROR ***** File write error.(c32datawrite)\n");
                    iErr = 1;
                    break; 
                }
                kkkkkk++;
            }
        }  /** for (ia=0; ia<*piNchannel; ia++) **/
    }  /** if (iErr == 0) **/
    if (iHandle != 1) close(iHandle);     /** 標準出力以外だったらクローズ **/
    if(pucDat != NULL) {
        free(pucDat);
        pucDat = NULL;
    }
}

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
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <s8c32_type.h>
#include <s8c32_prot.h>
#define MAXBYTE 5000000
typedef union __UNION_VAR
{
    int  i;
    unsigned int ui;
    int l;
    unsigned int ul;
    float f;
    double d;
    short int h;
    unsigned short int uh;
    char c[4];
    char * pc;
    void * pv;
    unsigned char * puc;
} UNION_VAR;
extern int igTest;
int c32dataread_write(
    int           iKbeginfile,     /** ( I ) 最初のファイルか **/
    char        * pcFilename_out,  /** ( I ) 読み込むＷＩＮ３２データファイル名 **/
    char        * pcFilename_in,   /** ( I ) 読み込むＷＩＮ３２データファイル名 **/
    int         *piHandle_out,
    int         *piHandle_in
)
{
    unsigned short int uhOrg;
    unsigned char ucDat_w[16];
/*     static unsigned char * pucDat = NULL; */
    static UNION_VAR uni;
    static int iMaxbyte = 0;
    int iBsize;
    int iSize;
    int iRet;
    int iKer;
#ifdef MINGW
    int result;
#endif
    fprintf(stderr, "%s\n", pcFilename_in);
    iRet = 1;
    uni.puc = NULL;
    if (pcFilename_out[0] == '\0') {  /** ＮＵＬＬの場合？ **/
        *piHandle_out = 1;              /** 標準出力にする **/
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
        if (iKbeginfile == 1) {
#ifdef MINGW
            *piHandle_out = open(pcFilename_out, O_WRONLY | O_CREAT | O_TRUNC | O_BINARY,0666 );
#else
            *piHandle_out = open(pcFilename_out, O_WRONLY | O_CREAT | O_TRUNC ,0666 );
#endif
                                      /** 指定ファイルをオープン **/
            if ( *piHandle_out == -1 ) {
                fprintf (stderr, "***** ERROR ***** The file open error.(%s)(c32dataread_write)\n",
                         pcFilename_out );
                goto ret;
            }
        }
    }
    if (strcmp(pcFilename_in, "-") == 0) {
        *piHandle_in = 0;                       /** 標準入力 **/
#ifdef MINGW
       /* "stdin" をバイナリ モードに設定します。 */
        result=_setmode(_fileno(stdin),_O_BINARY);
        if( result == -1 ) {
            fprintf(stderr, "***** ERROR ***** The mode does not set.(%s %d)\n",
                    __FILE__, __LINE__);
           exit(0);
        }
#endif
    } else {
#ifdef MINGW
        *piHandle_in = open(pcFilename_in, O_RDONLY | O_BINARY);
#else
        *piHandle_in = open(pcFilename_in, O_RDONLY);
#endif
        if ( *piHandle_in == -1 ) {
            fprintf (stderr, "***** ERROR ***** The file open error.(%s)(c32dataread_write)\n",
                     pcFilename_in ) ;
            goto ret;
        }
    }
    /* トップデータ */
    iSize = read ( *piHandle_in , ucDat_w , (size_t) 4 ) ;
    if ( iSize != 4 ) {
        fprintf (stderr, "***** ERROR ***** The file read error.(%s)(c32dataread_write)\n",
                 pcFilename_in ) ;
        goto ret;
    }
    /** トップ部分を書き込む **/
    if (iKbeginfile == 1) {
        iSize = write(*piHandle_out, ucDat_w, (size_t)4);
        if (iSize != 4) {
            fprintf(stderr, "***** ERROR ***** The file write error.(c32datawrite)\n");
            goto ret;
        }
    }
    while (1) {
        iSize = read ( *piHandle_in , ucDat_w , (size_t) 16 ) ;
        if ( iSize != 16 ) break;            /** 終了 **/
        memmove(&iBsize, &ucDat_w[12], 4);
/* printf("iSize=[%d] iBsize=[%d]\n", iSize, iBsize); */
/*         bytrev_((unsigned char *)&iBsize, &i04); */
        swap4b((unsigned int *)&iBsize);
/* printf("iSize=[%d] iBsize=[%d]\n", iSize, iBsize); */
        if (iBsize > MAXBYTE) {
            fprintf(stderr,
                 "***** ERROR ***** The channel block size is maximum over.(%d)(c32datawrite)\n",
                 MAXBYTE);
            goto ret;
        }
        iSize = write(*piHandle_out, ucDat_w, (size_t)16);
        if (iSize != 16) {
            fprintf(stderr, "***** ERROR ***** The file write error.(c32datawrite)\n");
            goto ret;
        }
        if (iBsize >= MAXBYTE) {
            fprintf(stderr, "***** ERROR ***** The data block length is over maximum. (%d)(%s %d)\n",
                    MAXBYTE, __FILE__, __LINE__);
            exit (0);
        }
        if (uni.puc != NULL) {
            free(uni.puc);
            uni.puc = NULL;
            iMaxbyte = 0;
        }
        iKer = maxalloc((void **)&uni.pv, MAXBYTE, &iMaxbyte);
        if (iKer) {
            fprintf (stderr, "***** ERROR ***** Meomory allocation error.(%d)(c32dataread_write)\n",
                             MAXBYTE );
            goto ret;
        }
        iSize = read ( *piHandle_in , uni.puc , (size_t) iBsize ) ; 
/* printf("iSize=[%d] iBsize=[%d]\n", iSize, iBsize); */
        if ( iSize != iBsize ) {
            fprintf(stderr, "***** ERROR ***** The %d byte data read error.(c32datawrite)\n",
                    iBsize);
            goto ret;
        }
        memmove(&uhOrg, uni.puc, 2);
/*         if (igTest == 2) { */
/*             uhOrg = 0x0809; */
/*             memmove(uni.puc, &uhOrg, 2); */
/*         } */
        iSize = write(*piHandle_out, uni.puc, (size_t)iBsize);
        if (iSize != iBsize) {
            fprintf(stderr, "***** ERROR ***** The %d byte data write error.(c32datawrite)\n",
                            iBsize);
            goto ret;
        }
    }  /** while (1) **/
    iRet = 0;
ret:;
    if (*piHandle_in != 0) close(*piHandle_in);  /** 標準入力でなければクローズ **/
    if (uni.puc != NULL) {
        free(uni.puc);
        uni.puc = NULL;
        iMaxbyte = 0;
    }
    return iRet;
}

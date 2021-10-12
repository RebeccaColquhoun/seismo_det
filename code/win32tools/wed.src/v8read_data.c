#include <string.h>
#include <stdlib.h>
#include <v8winlib.h>
#include <v8wed_ext.h>
extern int giKbegin;
extern int giKwin32;
int 
read_data()
{
    size_t iSizet;
    static unsigned int size;
    static unsigned int size2;
    unsigned char timestmp[6];
    int     re;
    int     iRet;
    unsigned char ucDat[20];
    iSizet = fread(&re, 1, 4, stdin);
    if (iSizet != 4) {
        iRet = 0;
        goto ret;
    } else {
        if (giKbegin == 1) {
            giKbegin = 0;
            if (re == 0) {
                giKwin32 = 1;            
                if (fread(&re, 1, 4, stdin) != 4) {
                    iRet = 0;
                    goto ret;
                }
            }
        }
    }
    if (giKwin32 == 1) {
        memmove(ucDat, &re, 4);
        iSizet = fread(&ucDat[4], 1, 12, stdin);
        if (iSizet != 12) {
            iRet = 0;
            goto ret;
        }
        memmove(&re, &ucDat[12], 4);
    }
    re = IntFromBigEndian(re);
    if (buf == 0) {
        size = 5000000 * 2;
        buf = (unsigned char *) malloc(size+100);  /** freadで余分に読むため **/
        outbuf = (unsigned char *) malloc(size+100); /** freadで余分に読むため **/
    } else if (re > size) {
        size = re * 2;
        buf = (unsigned char *) realloc(buf, size+100); /** freadで余分に読むため **/
        outbuf = (unsigned char *) realloc(outbuf, size+100); /** freadで余分に読むため **/
    }
    if (buf == NULL || outbuf == NULL) {
        printf("***** ERROR ***** The memory allocation error.(%d)(%s %d)\n",
                                                    size+100, __FILE__, __LINE__);
        exit (0);
    }
    if (giKwin32 == 0) {
        *(int *) buf = re;
        iSizet = fread(buf + 4, 1, re - 4, stdin);
        if (iSizet != re-4) {
            iRet = 0;
            goto ret;
        }
    } else {
        *(int *) buf = re+16;                 /** 先頭は全体の個数 **/
        memmove(buf + 4, ucDat, 16);           /** 次はヘッダー（１６バイト） **/
        iSizet = fread(buf + 20, 1, re, stdin);/** 次はチャネルブロック **/
        if (iSizet != re) {
            iRet = 0;
            goto ret;
        }
        re = re + 16;
    }
    if (giKwin32 == 0) {
        /* win2? --> win2 or win1? --> win1  990603 add by nishiyma */
        if (WinGetVersion(buf + 10) == 2) {
            size2 = Win2UpkSecSize(buf + 10, re - 6);
            if (size2 + 10 > size) {
                outbuf = (unsigned char *) realloc(outbuf, size = (size2 + 10));
            }
            size2 = Win2UpkSec(buf + 10, re - 6, outbuf);
            memcpy(timestmp, buf + 4, 6);
            if (size2 + 10 > size) {
                buf = (unsigned char *) realloc(buf, size = (size2 + 10));
            }
            memcpy(buf + 4, timestmp, 6);
            memcpy(buf + 10, outbuf, size2);
            *(int *) buf = (size2 + 10);
        }                                   /*----------------*/
    }
    iRet = re;
ret:;
    return iRet;
}

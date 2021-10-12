#include <string.h>
#include <stdlib.h>
#include <y1wch_n_man.h>
#include <y1wch_prot.h>
extern int     giKbegin;
extern int     giKwin32;
extern int     giKwrite;
int read_data()
{
    size_t iSizet;
    unsigned char ucDat[20];
    static unsigned int size;
    int     re;
    int     iRet;
    int     re1;
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
    swap4b((unsigned int *)&re);
    if (buf == 0) {
        size = re * 2;
        buf = (unsigned char *) malloc(size+100);     /** freadで余分に読むため **/
        outbuf = (unsigned char *) malloc(size+100);  /** freadで余分に読むため **/
    } else if (re > size) {
        size = re * 2;
        buf = (unsigned char *) realloc(buf, size+100); /** freadで余分に読むため **/
        outbuf = (unsigned char *) realloc(outbuf, size+100); /** freadで余分に読むため **/
    }
    if (buf == NULL || outbuf == NULL) {
        fprintf(stderr, "***** ERROR ***** The memory allocation error.(%d)(%s %d)\n",
                                                    size+100, __FILE__, __LINE__);
        exit (0);
    }
    if (giKwin32 == 1) {
        re += 16;
    }
    re1 = re;
    swap4b((unsigned int *)&re1);
    *(int *) buf = re1;     /** 正数でない **/
    if (giKwin32 == 0) {
        re = fread(buf + 4, 1, re - 4, stdin);  /** re は、re-4になる **/
    } else {
        memmove(buf + 4, ucDat, 16);           /** 次はヘッダー（１６バイト） **/
        iSizet = fread(buf + 20, 1, re-16, stdin);/** 次はチャネルブロック **/
        if (iSizet != re-16) {
            iRet = 0;
            goto ret;
        }
    }
    iRet = re;
ret:;
    return iRet;
}

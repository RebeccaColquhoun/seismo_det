#include <string.h>
#include <stdlib.h>
#include <v9dewin_ext.h>
extern int giKbegin;
extern int giKwin32;
int read_data(unsigned char **ptr, FILE *fp)
{
    static unsigned int size;
    int     re;
    int     iRet;
    size_t iSizet;
    unsigned char ucDat[20];
#if 0
#if    BYTE_ORDER == LITTLE_ENDIAN
    SWAPU;
#endif
#endif
    iSizet = fread(&re, 1, 4, fp);
    if (iSizet != 4) {
        iRet = 0;
        goto ret;
    } else {
        if (giKbegin == 1) {
            giKbegin = 0;
            if (re == 0) {
                giKwin32 = 1;
                if (fread(&re, 1, 4, fp) != 4) {
                    iRet = 0;
                    goto ret;
                }
            }
        }
    }
    if (giKwin32 == 1) {
        memmove(ucDat, &re, 4);
        iSizet = fread(&ucDat[4], 1, 12, fp);
        if (iSizet != 12) {
            iRet = 0;
            goto ret;
        }
        memmove(&re, &ucDat[12], 4);
    }
#if 0
#if    BYTE_ORDER == LITTLE_ENDIAN
    SWAPL(re);
#endif
#else
    swap4b((unsigned int *)&re);
#endif
    if (*ptr == 0) {
        size = re * 2;
        *ptr = (unsigned char *) malloc(size+100); /** freadで余分に読むため **/
    } else if (re > size) {
        size = re * 2;
        *ptr = (unsigned char *) realloc(*ptr, size+100); /** freadで余分に読むため **/
    }
    if (*ptr == NULL) {
        fprintf(stderr, "***** ERROR ***** The memory allocation error.(%d)(%s %d)\n",
                                                    size+100, __FILE__, __LINE__);
        exit (1);
    }
    if (giKwin32 == 0) {
        *(int *) *ptr = re;
        iSizet = fread(*ptr + 4, 1, re - 4, fp);
        if (iSizet != re-4) {
            iRet = 0;
            goto ret;  
        }
    } else {
        *(int *) *ptr = re+16;                 /** 先頭は全体の個数 **/
        memmove(*ptr + 4, ucDat, 16);           /** 次はヘッダー（１６バイト） **/
        iSizet = fread(*ptr + 20, 1, re, fp);/** 次はチャネルブロック **/
        if (iSizet != re) {
            iRet = 0;
            goto ret;
        }
        re += 16;
    }
    iRet = re;
ret:;
    return iRet;
}

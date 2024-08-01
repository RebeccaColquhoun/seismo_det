#include <y0wadd_n_man.h>
extern int giKbegin_main;  
extern int giKbegin_sub;
extern int giKwin32_main;
extern int giKwin32_sub;
extern int giKwin32_both;
extern int giKwrite;
int read_data_main(unsigned char *ptr, FILE   *fp)
{
    int     ia;
    int     iRet;
    int     re;
/*     static unsigned int size; */
    size_t iSizet;
    unsigned char ucDat[20];
    iSizet = fread(ptr, 1, 4, fp);
    if (iSizet != 4) {
        iRet = 0;
        goto ret;
    } else {
        memmove(&re, ptr, 4);
        if (giKbegin_main == 1) {
            giKbegin_main = 0;
            if (re == 0) {
                giKwin32_main = 1;
                giKwin32_both = 1;
                if (fread(ptr, 1, 4, fp) != 4) {
                    iRet = 0;
                    goto ret;
                }
            }
        }
    }
    if (giKwin32_main == 1) {                 
        memmove(ucDat, ptr, 4);
        iSizet = fread(&ucDat[4], 1, 12, fp);
        if (iSizet != 12) {
            iRet = 0;
            goto ret;
        }
        memmove(ptr, &ucDat[12], 4);
        for (ia=0; ia<8; ia++) {
        }
    }
    memmove(&re, ptr, 4);
    swap4b((unsigned int *)&re);
    if (giKwin32_main == 0) {
        if (fread(ptr + 4, 1, re - 4, fp) != re-4) {
            iRet = 0;
            goto ret;
        }
    } else {
        memmove(ptr + 4, ucDat, 16);           /** 次はヘッダー（１６バイト） **/
        iSizet = fread(ptr + 20, 1, re, fp);/** 次はチャネルブロック **/
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

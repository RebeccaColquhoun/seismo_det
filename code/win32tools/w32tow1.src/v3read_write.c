#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include <v3win32_type.h>
#include <v3win32_prot.h>
/* #include <ape_define.h> */
    
#define MAXBYTE 10000000
int
read_write(
    FILE * psFile_in,
    FILE * psFile_out
)
{
/*     unsigned char ucDat[MAXBYTE]; */
    unsigned char *ucDat = NULL;
    int iCount;
    int iDummy;
    int iBsize;
    unsigned char * pucAdr;
    unsigned char * pucEnd;
    unsigned short uhChno;
    int iKer;
    int iOffsize;
    int iNsampno;
    int iRet;
    fpos_t iPos;
    fpos_t iPosend;
    int iTotbyte;
    int iTotbyte_w;
    int iAllbyte;
    iRet = 1;
    if (ucDat != NULL) {
        free(ucDat);
    }
    ucDat = (unsigned char *) malloc(sizeof(char)*MAXBYTE);
    if (ucDat == NULL) {
        printf("***** ERROR ***** The memory alloc error.(%s %d)\n", __FILE__, __LINE__);
        exit (0);
    }
    /** フォーマット部分読み込み **/
    iCount = fread(ucDat, 1, 4, psFile_in);
    if (iCount != 4) {
        printf("***** ERROR ***** File read error.(%d)(%s %d)\n", 4, __FILE__, __LINE__);
        goto ret;
    }
    if (*((int *)ucDat) != 0) {
        printf("***** ERROR ***** This file is not win32 data.(%d)(%s %d)\n", *((int *)ucDat), __FILE__, __LINE__);
        goto ret;
    }
    while (1) {
        iCount = fread(ucDat, 1, 16, psFile_in);
        if (iCount != 16) break;
        iCount = fgetpos(psFile_out, (fpos_t *)&iPos);
        if (iCount != 0) {
            printf("***** ERROR ***** File getpos error.(%s %d)\n", __FILE__, __LINE__);
            goto ret;
        }
        iCount = fwrite(&iDummy, 1, 4, psFile_out);
        if (iCount != 4) {
            printf("***** ERROR ***** File write error.(%d)(%s %d)\n", 4, __FILE__, __LINE__);
            goto ret;
        }
        memmove(&iBsize, &ucDat[12], 4);
/*         bytrev_((unsigned char *)&iBsize, &i04); */
        swap4b((unsigned int *)&iBsize);
    
        if (iBsize > MAXBYTE) {
            printf("***** ERROR ***** data block length maximun over.(%d/%d)(%s %d)\n", iBsize, MAXBYTE, __FILE__, __LINE__);
            goto ret;
        }
        /** 日付書き込み **/
        iCount = fwrite(&ucDat[1], 1, 6, psFile_out);
        if (iCount != 6) {
            printf("***** ERROR ***** File write error.(%d)(%s %d)\n", 6, __FILE__, __LINE__);
            goto ret;
        }
    
        /** 時間フレーム読み込み **/
        iCount = fread(ucDat, 1, iBsize, psFile_in);
        if (iCount != iBsize) {
            printf("***** ERROR ***** File read error.(%d)(%s %d)\n", iBsize, __FILE__, __LINE__);
            goto ret;
        }
    
        pucAdr = &ucDat[0];
        pucEnd = &ucDat[0] + iBsize;
        iTotbyte = 0;
        while (pucAdr < pucEnd) {
            pucAdr += 2;
            iKer = winget_chnl(pucAdr, &uhChno, &iOffsize, &iNsampno, &iAllbyte);
            if (iKer) {
                printf("***** ERROR ***** Win32 data read error.(%s %d)\n", __FILE__, __LINE__);
                goto ret;
            }
            iCount = fwrite(pucAdr, 1, iAllbyte, psFile_out);
            if (iCount != iAllbyte) {
                printf("***** ERROR ***** File write error.(%d)(%s %d)\n", iAllbyte, __FILE__, __LINE__);
                goto ret;
            }
            iTotbyte += iAllbyte;
            pucAdr += iAllbyte;
        }
        iCount = fgetpos(psFile_out, (fpos_t *)&iPosend);
        if (iCount != 0) {
            printf("***** ERROR ***** File getpos error.(%s %d)\n", __FILE__, __LINE__);
            goto ret;
        }
        iCount = fsetpos(psFile_out, (fpos_t *)&iPos);
        if (iCount != 0) {
            printf("***** ERROR ***** File setpos error.(%s %d)\n", __FILE__, __LINE__);
            goto ret;
        }
        iTotbyte += 10;
        iTotbyte_w = iTotbyte;
/*         bytrev_((unsigned char *)&iTotbyte_w, &i04); */
        swap4b((unsigned int *)&iTotbyte_w);
        iCount = fwrite(&iTotbyte_w, 1, 4, psFile_out);
        if (iCount != 4) {
            printf("***** ERROR ***** File write error.(%d)(%s %d)\n", iTotbyte, __FILE__, __LINE__);
            goto ret;
        }
        iCount = fsetpos(psFile_out, (fpos_t *)&iPosend);
        if (iCount != 0) {
            printf("***** ERROR ***** File setpos error.(%s %d)\n", __FILE__, __LINE__);
            goto ret;
        }
    }
    iRet = 0;
ret:;
    return iRet;
}

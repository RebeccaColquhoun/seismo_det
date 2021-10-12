#include <stdlib.h>
#include <v7wck_man.h>
extern int giKbegin;   
extern int giKwin32;   
extern int giKprint;   
extern int giKrawprint;   
extern int giKwidechan;   
extern int giTime[6];
extern unsigned int guiNoch;
extern int win2fix( unsigned char *pucPtr, int *piAbuf, unsigned int *puhChanno, int *piNsampno);
int read_data(unsigned char **ppucPtr, FILE   *ptFp)
{
    int iii = 0;
    int jjj;
    int iKpr;
    unsigned char * pucLast;
    unsigned char * pucStart;
    int iAbyte;
    int iNrow;
    int iNsamp;
    unsigned int uiCno;
    int iAbuf[5000];
    size_t iSizet;
    unsigned char ucDat[20];
    static unsigned int uiSize;
    int     iRe;
    int     iRet;
    int     ia;
    int     ib;
    int     iDate[8];
    unsigned char uc1;
    unsigned char uc2;
#if 0
    iSizet = fread(ucDat, 1, 20, ptFp);
    iPos = 0;
    fsetpos(ptFp, &iPos);
    for (ia=0; ia<20; ia++) {
    }
#endif
    iSizet = fread(&iRe, 1, 4, ptFp);
    if (iSizet != 4) {
        iRet = 0;
        goto ret;
    } else {
        if (giKbegin == 1) {
            giKbegin = 0;
            if (iRe == 0) {
                giKwin32 = 1;
                if (fread(&iRe, 1, 4, ptFp) != 4) {
                    iRet = 0;
                    goto ret;
                }
            }
        }
    }
    if (giKwin32 == 1) {
        memmove(ucDat, &iRe, 4);
        iSizet = fread(&ucDat[4], 1, 12, ptFp);
        if (iSizet != 12) {
            iRet = 0;
            goto ret;
        }
        memmove(&iRe, &ucDat[12], 4);
#if 0
        for (ia=0; ia<8; ia++) { 
            uc1= ucDat[ia] & 0xf0;
            uc1 = uc1 >> 4;
            uc2= ucDat[ia] & 0x0f;
            iDate[ia]=uc1*10+uc2;
        }
        for (ia=0; ia<16; ia++) {
        }
#endif
    }
    iRe = IntFromBigEndian(iRe);
    if (*ppucPtr == 0) {               /** まだALLOCしていない時 **/
        uiSize = 500000 * 2;
        *ppucPtr = (unsigned char *) malloc((size_t)(uiSize+100)); /** freadで余分に読むため **/
    } else if (iRe > uiSize) {         /** ALLOCしているが、サイズが足りない時 **/
        uiSize = iRe * 2;
        *ppucPtr = (unsigned char *) realloc(*ppucPtr, (size_t)(uiSize+100)); /** freadで余分に読むため **/
    }
    if (*ppucPtr == NULL) {
        printf("***** ERROR ***** Memory alloc error.(%d)(%s %d)\n",
                 uiSize+100, __FILE__, __LINE__);
        exit (0);
    }
    if (giKwin32 == 0) {
        *(int *) *ppucPtr = iRe;
        if (fread(*ppucPtr + 4, 1, iRe - 4, ptFp) != iRe-4) {
            iRet = 0;
            goto ret;
        }
    } else {
        *(int *) *ppucPtr = iRe+16;                 /** 先頭は全体の個数 **/
        memmove(*ppucPtr + 4, ucDat, 16);           /** 次はヘッダー（１６バイト） **/
        iSizet = fread(*ppucPtr + 20, 1, iRe, ptFp);/** 次はチャネルブロック **/
        if (iSizet != iRe) {
            iRet = 0;
            goto ret;
        }
        iRe = iRe + 16;
    }
    if (giKprint != 0) {
        pucStart = *ppucPtr+4;
        if (giKwin32 == 1) pucStart = *ppucPtr+5;
        for (ia=0; ia<6; ia++) {
            uc1= pucStart[ia] & 0xf0;
            uc1 = uc1 >> 4;
            uc2= pucStart[ia] & 0x0f;
            iDate[ia]=uc1*10+uc2;
        }
        if (iDate[0] > 50) {
            iDate[0] += 1900;
        } else {
            iDate[0] += 2000;
        }
        pucLast = *ppucPtr + iRe;
        pucStart = *ppucPtr + 10;
        if (giKwin32 == 1) {
            pucLast = *ppucPtr + 4 + iRe;
            pucStart = *ppucPtr + 4 + 16 + 2;
        }
        while(pucStart < pucLast) {
            iAbyte = win2fix(pucStart, iAbuf, &uiCno, &iNsamp);
            if (iAbyte == 0) {                        
                printf("***** ERROR ***** The data of win32 error.");
                exit (1);
            }
            iKpr = 0;
            if (giKprint == 1) {
                iKpr = 1;
            } else if (giKprint == 2) {
                if (giTime[0] == iDate[0] &&
                    giTime[1] == iDate[1] &&
                    giTime[2] == iDate[2] &&
                    giTime[3] == iDate[3] &&
                    giTime[4] == iDate[4] &&
                    giTime[5] == iDate[5]) {
                    iKpr = 1;
                }
            } else if (giKprint == 3) {
                if (uiCno == guiNoch) {
                    iKpr = 1;
                }
            } else if (giKprint == 4) {
                if (uiCno == guiNoch &&
                    giTime[0] == iDate[0] &&
                    giTime[1] == iDate[1] &&
                    giTime[2] == iDate[2] &&
                    giTime[3] == iDate[3] &&
                    giTime[4] == iDate[4] &&
                    giTime[5] == iDate[5]) {
                    iKpr = 1;
                }
            }
                
            if (iKpr == 1) {
                fprintf(stderr,"DATE=%04d/%02d/%02d %02d:%02d:%02d ", iDate[0], iDate[1], iDate[2],
                                                              iDate[3], iDate[4], iDate[5]);
                if (giKwidechan == 0) {
                    fprintf(stderr,"CHNO=%04x SAMPLE NO.=%4d\n", uiCno, iNsamp);
                } else {
                    fprintf(stderr,"CHNO=%08x SAMPLE NO.=%4d\n", uiCno, iNsamp);
                }
    
                iNrow = (iNsamp-1)/10+1; 
                fprintf(stderr,"SAMPLE DATA:\n");
                for (ia=0; ia<iNrow; ia++) {
                    for (ib=ia*10; (ib<(ia+1)*10 && ib<iNsamp); ib++) {
                        jjj = iAbuf[ib];
                        if (ib != 0 && giKrawprint == 1) {
                            jjj = jjj - iii;
                        }
                        fprintf(stderr,"%10d", jjj);
                        iii = iAbuf[ib];
                    }
                    fprintf(stderr,"\n");
                }
            }
            if (giKwin32 == 0) {
                pucStart = pucStart + iAbyte;
            } else {
                pucStart = pucStart + iAbyte + 2;
            }
        }
    }
    iRet = iRe;
ret:;
    return iRet;
}

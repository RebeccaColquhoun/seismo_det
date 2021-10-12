#include <string.h>
#include <stdio.h>
#include <stdlib.h>
/** １チャンネル分のＷＩＮ１データを取り出す **/
/** BIG_ENDIAN, SMALL_ENDIAN の両方に対応している **/
extern void swap2b(unsigned short *pic);
extern int giKwidechan;
int 
win2fix(                                /* チャンネルデータの全バイト数 */
    unsigned char *pucPtr,              /* ( I ) チャンネルデータ
                                         *      （チャンネル番号から） */
    int *piAbuf,                        /* ( O ) サンプルデータ */
    unsigned *puiChanno,          /* ( O ) チャンネル番号 */
    int *piNsampno                      /* ( O ) サンプリング数 */
)
{
    int     iRet;
    int     iB_size;
    int     iG_size;
    int     iI;
    int     iS_rate;
    unsigned char *pucDp;
    unsigned int uiGh;
    unsigned short int uhCh0;
    short   hShreg;
    int     iInreg;
    pucDp = pucPtr;
    if (giKwidechan == 1) {
        memmove(&uhCh0, pucPtr-2, 2);
        swap2b((unsigned short int *)&uhCh0);
    }
    uiGh = ((pucDp[0] << 24) & 0xff000000) + ((pucDp[1] << 16) & 0xff0000) +
        ((pucDp[2] << 8) & 0xff00) + (pucDp[3] & 0xff);
    pucDp += 4;
    iS_rate = uiGh & 0xfff;
    *piNsampno = iS_rate;
    if ((iB_size = (uiGh >> 12) & 0xf) != 0) {
        iG_size = iB_size * (iS_rate - 1) + 8;
    } else {
        iG_size = (iS_rate >> 1) + 8;
    }
    if (giKwidechan == 0) {
        *puiChanno = (unsigned int) ((uiGh >> 16) & 0xffff);
    } else {
        *puiChanno = uhCh0 << 16;
        *puiChanno = *puiChanno | ((uiGh >> 16) & 0xffff);
    }
/*     if (*puiChanno == (unsigned short)0x5902) { */
/*     } */
    /* read group */
    piAbuf[0] = ((pucDp[0] << 24) & 0xff000000) + ((pucDp[1] << 16) & 0xff0000) +
        ((pucDp[2] << 8) & 0xff00) + (pucDp[3] & 0xff);
    pucDp += 4;
    if (iS_rate == 1) {
        iRet = iG_size;                 /* normal return */
        goto ret;
    }
    if (iS_rate > 1000) {
        fprintf(stderr,"***** ERROR ***** The rate is maximum over.(%d,%d)\n",
                       iS_rate, 1000);
        fflush(stderr);
        exit (1);
    }
        
    switch (iB_size) {
    case 0:
        for (iI = 1; iI < iS_rate; iI += 2) {
            piAbuf[iI] = piAbuf[iI - 1] + ((*(char *) pucDp) >> 4);
            if (iI+1 < iS_rate) {
                piAbuf[iI + 1] = piAbuf[iI] + (((char) (*(pucDp++) << 4)) >> 4);
            }
        }
        break;
    case 1:
        for (iI = 1; iI < iS_rate; iI++) {
            piAbuf[iI] = piAbuf[iI - 1] + (*(char *) (pucDp++));
        }
        break;
    case 2:
        for (iI = 1; iI < iS_rate; iI++) { 
/*             if (*puiChanno == (unsigned int)0x5902) { */
/*             } */
            hShreg = ((pucDp[0] << 8) & 0xff00) + (pucDp[1] & 0xff);
            pucDp += 2;
            piAbuf[iI] = piAbuf[iI - 1] + hShreg;
/*             if (*puiChanno == (unsigned int)0x5902) { */
/*             } */
        }
        break;
    case 3:
        for (iI = 1; iI < iS_rate; iI++) {
            iInreg = ((pucDp[0] << 24) & 0xff000000) + ((pucDp[1] << 16) & 0xff0000) +
                ((pucDp[2] << 8) & 0xff00);
            pucDp += 3;
            piAbuf[iI] = piAbuf[iI - 1] + (iInreg >> 8);
        }
        break;
    case 4:
        for (iI = 1; iI < iS_rate; iI++) {
            iInreg = ((pucDp[0] << 24) & 0xff000000) + ((pucDp[1] << 16) & 0xff0000) +
                ((pucDp[2] << 8) & 0xff00) + (pucDp[3] & 0xff);
            pucDp += 4;
            piAbuf[iI] = piAbuf[iI - 1] + iInreg;
        }
        break;
    default:
        iRet = 0;                       /* bad header */
        goto ret;
    }
    iRet = iG_size;                     /* normal return */
ret:;
    return iRet;
}

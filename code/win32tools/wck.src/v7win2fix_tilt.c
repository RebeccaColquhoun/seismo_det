#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
/** １チャンネル分のＷＩＮ１(TILT)データを取り出す **/
/** BIG_ENDIAN, SMALL_ENDIAN の両方に対応している **/
int 
win2fix_tilt(                                /* チャンネルデータの全バイト数 */
    unsigned char *pucPtr,              /* ( I ) チャンネルデータ
                                         *      （チャンネル番号から） */
    int *piAbuf,                        /* ( O ) サンプルデータ */
    unsigned short *puhChanno,          /* ( O ) チャンネル番号 */
    int *piNsampno                      /* ( O ) サンプリング数 */
)
{
    int     iMinint;
    int     iKreal;
    int     iSamp1;
    int     iSamp;
    int     iRet;
    int     iB_size;
    int     iG_size;
    int     iI;
    int     iS_rate;
    unsigned char *pucDp;
    unsigned int uiGh;
    short   hShreg;
    int     iInreg;
    iMinint = INT_MIN;
    pucDp = pucPtr;
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
    *puhChanno = (unsigned short) ((uiGh >> 16) & 0xffff);
    if (*puhChanno == (unsigned short)0x5902) {
    }
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
        
	iSamp1 = piAbuf[0];
    switch (iB_size) {
    case 0:
        for (iI = 1; iI < iS_rate; iI += 2) {
            iSamp = (int)((*(char *) pucDp) >> 4);
            if (iSamp == -8) {
				piAbuf[iI] = iMinint;
			} else {
				piAbuf[iI] = iSamp1 + iSamp;
				iSamp1 = piAbuf[iI];
			}
/*             piAbuf[iI] = piAbuf[iI - 1] + ((*(char *) pucDp) >> 4); */
            if (iI+1 < iS_rate) {
                iSamp = (int)(((char) (*(pucDp++) << 4)) >> 4);
	            if (iSamp == -8) {
	                piAbuf[iI+1] = iMinint;
	            } else {
	                piAbuf[iI+1] = iSamp1 + iSamp;
	                iSamp1 = piAbuf[iI+1];
	            }
/*                 piAbuf[iI + 1] = piAbuf[iI] + (((char) (*(pucDp++) << 4)) >> 4); */
            }
        }
        break;
    case 1:
        for (iI = 1; iI < iS_rate; iI++) {
			iSamp = (int)(*(char *) (pucDp++));
			if (iSamp == -128) {
				piAbuf[iI] = iMinint;
			} else {
				piAbuf[iI] = iSamp1 + iSamp;
				iSamp1 = piAbuf[iI];
			}
/*             piAbuf[iI] = piAbuf[iI - 1] + (*(char *) (pucDp++)); */
        }
        break;
    case 2:
        for (iI = 1; iI < iS_rate; iI++) { 
            hShreg = ((pucDp[0] << 8) & 0xff00) + (pucDp[1] & 0xff);
            pucDp += 2;
			iSamp = (int)hShreg;
			if (iSamp == -32768) {
				piAbuf[iI] = iMinint;
			} else {
				piAbuf[iI] = iSamp1 + iSamp;
				iSamp1 = piAbuf[iI];
			}
/*             piAbuf[iI] = piAbuf[iI - 1] + hShreg; */
        }
        break;
    case 3:
        for (iI = 1; iI < iS_rate; iI++) {
            iInreg = ((pucDp[0] << 24) & 0xff000000) + ((pucDp[1] << 16) & 0xff0000) +
                ((pucDp[2] << 8) & 0xff00);
            pucDp += 3;
			iSamp = (iInreg >> 8);
			if (iSamp == -8388608) {
				piAbuf[iI] = iMinint;
			} else {
				piAbuf[iI] = iSamp1 + iSamp;
				iSamp1 = piAbuf[iI];
			}
/*             piAbuf[iI] = piAbuf[iI - 1] + (iInreg >> 8); */
        }
        break;
    case 4:
		iKreal = 0;           /** 正常値は、まだない **/
		if (iSamp1 != iMinint) iKreal = 1;        /** 正常値があった **/
        for (iI = 1; iI < iS_rate; iI++) {
            iInreg = ((pucDp[0] << 24) & 0xff000000) + ((pucDp[1] << 16) & 0xff0000) +
                ((pucDp[2] << 8) & 0xff00) + (pucDp[3] & 0xff);
            pucDp += 4;
			iSamp = iInreg;
			if (iSamp == iMinint) {
				piAbuf[iI] = iMinint;
			} else {
				if (iKreal == 1) {  /** 正常値が既にあった場合 **/
					piAbuf[iI] = iSamp1 + iSamp;
					iSamp1 = piAbuf[iI];
				} else {            /** まだ正常値がない場合 **/
					piAbuf[iI] = iSamp;
					iSamp1 = piAbuf[iI];
					iKreal = 1;
				}
			}
/*             piAbuf[iI] = piAbuf[iI - 1] + iInreg; */
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

#include <stdlib.h>
#include <y0wadd_prot.h>
/** �������ͥ�ʬ�ΣףɣΣ��ǡ�������Ф� **/
/** BIG_ENDIAN, SMALL_ENDIAN ��ξ�����б����Ƥ��� **/
int 
win2fix(                                /* �����ͥ�ǡ��������Х��ȿ� */
    unsigned char *pucPtr,              /* ( I ) �����ͥ�ǡ���
                                         *      �ʥ����ͥ��ֹ椫��� */
    int *piAbuf,                        /* ( O ) ����ץ�ǡ��� */
    unsigned short *puhChanno,          /* ( O ) �����ͥ��ֹ� */
    int *piNsampno                      /* ( O ) ����ץ�󥰿� */
)
{
    int     iRet;
    int     iB_size;
    int     iG_size;
    int     iI;
    int     iS_rate;
    unsigned char *pucDp;
    unsigned int uiGh;
    short   hShreg;
    int     iInreg;
    pucDp = pucPtr;
    uiGh = (pucDp[0] << 24) + (pucDp[1] << 16) +
        (pucDp[2] << 8) + pucDp[3];
    pucDp += 4;
    iS_rate = uiGh & 0xfff;
    *piNsampno = iS_rate;
    if ((iB_size = (uiGh >> 12) & 0xf) != 0) {
        iG_size = iB_size * (iS_rate - 1) + 8;
    } else {
        iG_size = (iS_rate >> 1) + 8;
    }
    *puhChanno = (unsigned short) (uiGh >> 16);
    printf("channel no. %04x\n", *puhChanno);
/*     if (*puhChanno == (unsigned short)0x5902) { */
/*     } */
    /* read group */
    piAbuf[0] = (pucDp[0] << 24) + (pucDp[1] << 16) +
        (pucDp[2] << 8) + pucDp[3];
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
/*             if (*puhChanno == (unsigned short)0x5902) { */
/*             } */
            hShreg = (pucDp[0] << 8) + pucDp[1];
            pucDp += 2;
            piAbuf[iI] = piAbuf[iI - 1] + hShreg;
/*             if (*puhChanno == (unsigned short)0x5902) { */
/*             } */
        }
        break;
    case 3:
        for (iI = 1; iI < iS_rate; iI++) {
            iInreg = (pucDp[0] << 24) + (pucDp[1] << 16) +
                (pucDp[2] << 8);
            pucDp += 3;
            piAbuf[iI] = piAbuf[iI - 1] + (iInreg >> 8);
        }
        break;
    case 4:
        for (iI = 1; iI < iS_rate; iI++) {
            iInreg = (pucDp[0] << 24) + (pucDp[1] << 16) +
                (pucDp[2] << 8) + pucDp[3];
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

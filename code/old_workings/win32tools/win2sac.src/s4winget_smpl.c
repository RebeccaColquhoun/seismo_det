/************************************************************************
１チャンネル分のＷＩＮ１データからサンプルデータを取り出す
BIG_ENDIAN, SMALL_ENDIAN の両方に対応している
************************************************************************/
int
winget_smpl(
    unsigned char *pucPtr,              /* ( I ) チャンネルデータ （チ
                                         * ャンネル番号のアドレス） */
    int iOffsize,                       /* ( I ) サンプルサイズ(0---4) */
    int iNsampno,                       /* ( I ) サンプリング数 */
    int *piAbuf                         /* ( O ) サンプルデータ */
)
{
    int     iRet;
    int     iI;
    unsigned char *pucDp;
    short   hShreg;
    int     iInreg;
    iRet = 0;
    pucDp = pucPtr + 4;
    /* read group */
    piAbuf[0] = ((pucDp[0] << 24) & 0xff000000) + ((pucDp[1] << 16) & 0xff0000) +
        ((pucDp[2] << 8) & 0xff00) + (pucDp[3] & 0xff);
/*     exit(0); */
    pucDp += 4;
    switch (iOffsize) {
    case 0:
        for (iI = 1; iI < iNsampno; iI += 2) {
            piAbuf[iI] = piAbuf[iI - 1] + ((*(char *) pucDp) >> 4);
            if (iI+1 < iNsampno) {
                piAbuf[iI + 1] = piAbuf[iI] + (((char) (*(pucDp) << 4)) >> 4);
            }
            pucDp++;
        }
        break;
    case 1:
        for (iI = 1; iI < iNsampno; iI++) {
            piAbuf[iI] = piAbuf[iI - 1] + (*(char *) (pucDp));
            pucDp++;
        }
        break;
    case 2:
        for (iI = 1; iI < iNsampno; iI++) {
            hShreg = ((pucDp[0] << 8) & 0xff00) + (pucDp[1] & 0xff);
            pucDp += 2;
            piAbuf[iI] = piAbuf[iI - 1] + hShreg;
        }
        break;
    case 3:
        for (iI = 1; iI < iNsampno; iI++) {
            iInreg = ((pucDp[0] << 24) & 0xff000000) + ((pucDp[1] << 16) & 0xff0000) +
                ((pucDp[2] << 8) & 0xff00);
            pucDp += 3;
            piAbuf[iI] = piAbuf[iI - 1] + (iInreg >> 8);
        }
        break;
    case 4:
        for (iI = 1; iI < iNsampno; iI++) {
            iInreg = ((pucDp[0] << 24) & 0xff000000) + ((pucDp[1] << 16) & 0xff0000) +
                ((pucDp[2] << 8) & 0xff00) + (pucDp[3] & 0xff);
            pucDp += 4;
            piAbuf[iI] = piAbuf[iI - 1] + iInreg;
        }
        break;
    default:
        iRet = 1;
        break;
    }
    return iRet;
}

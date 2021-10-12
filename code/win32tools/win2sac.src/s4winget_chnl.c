/************************************************************************
１チャンネル分のＷＩＮ１データから
チャンネル番号・サンプルサイズ・サンプル数・全バイト数を取り出す
BIG_ENDIAN, SMALL_ENDIAN の両方に対応している
************************************************************************/
int
winget_chnl(
    unsigned char *pucPtr,              /* ( I ) チャンネルデータ （チ
                                         * ャンネル番号から） */
    unsigned short *puhSys_ch,          /* ( O ) チャンネル番号 */
    int *piOffsize,                     /* ( O ) サンプルサイズ(0---4) */
    int *piNsampno,                     /* ( O ) サンプリング数 */
    int *piAllbyte                      /* ( O ) 全バイト数 * */
)
{
    int     iRet;
    unsigned char *pucDp;
    unsigned int uiGh;
    iRet = 1;
    pucDp = pucPtr;
#if 0
    uiGh = ((pucDp[0] << 24) & 0xff000000) + ((pucDp[1] << 16) & 0xff0000) +
        ((pucDp[2] << 8) & 0xff00) + (pucDp[3] & 0xff);
#else
    uiGh = (pucDp[0] << 24) + (pucDp[1] << 16) +
        (pucDp[2] << 8) + pucDp[3];
#endif
    pucDp += 4;
    *piNsampno = uiGh & 0xfff;
    *piOffsize = (uiGh >> 12) & 0xf;
    if (*piOffsize != 0) {
        *piAllbyte = *piOffsize * (*piNsampno - 1) + 8;
    } else {
        *piAllbyte = (*piNsampno >> 1) + 8;
    }
#if 0
    *puhSys_ch = (unsigned short) ((uiGh >> 16) & 0xffff);
#else
    *puhSys_ch = (unsigned short) (uiGh >> 16);
#endif
    iRet = 0;
/*     if (*puhSys_ch == (unsigned short)0x2f53) { */
/*         printf("channo = %04x\n", *puhSys_ch); */
/*         printf("*piOffsize = %d\n", *piOffsize); */
/*         printf("*piNsampno = %d\n", *piNsampno); */
/*         printf("*piAllbyte = %d\n", *piAllbyte); */
/*     } */
        
    return iRet;
}

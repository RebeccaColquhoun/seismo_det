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
    uiGh = (pucDp[0] << 24) + (pucDp[1] << 16) +
        (pucDp[2] << 8) + pucDp[3];
    pucDp += 4;
    *piNsampno = uiGh & 0xfff;
    *piOffsize = (uiGh >> 12) & 0xf;
    if (*piOffsize != 0) {
        *piAllbyte = *piOffsize * (*piNsampno - 1) + 8;
    } else {
        *piAllbyte = (*piNsampno >> 1) + 8;
    }
    *puhSys_ch = (unsigned short) (uiGh >> 16);
    iRet = 0;
    return iRet;
}

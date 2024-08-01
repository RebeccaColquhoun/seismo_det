/************************************************************************
�������ͥ�ʬ�ΣףɣΣ��ǡ�������
�����ͥ��ֹ桦����ץ륵����������ץ�������Х��ȿ�����Ф�
BIG_ENDIAN, SMALL_ENDIAN ��ξ�����б����Ƥ���
************************************************************************/
int
winget_chnl(
    unsigned char *pucPtr,              /* ( I ) �����ͥ�ǡ��� �ʥ�
                                         * ���ͥ��ֹ椫��� */
    unsigned short *puhSys_ch,          /* ( O ) �����ͥ��ֹ� */
    int *piOffsize,                     /* ( O ) ����ץ륵����(0---4) */
    int *piNsampno,                     /* ( O ) ����ץ�󥰿� */
    int *piAllbyte                      /* ( O ) ���Х��ȿ� * */
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

#include <y0wadd_n_man.h>
extern int giKbegin_main;
extern int giKbegin_sub;
extern int giKwin32_main;
extern int giKwin32_sub;
extern int giKwin32_both;
extern int giKwrite;
/** WIN32�λ�����Ƭ�Υե����ޥå�����񤤤Ƥ��ʤ����Ͻ� **/
void check(
    int iSize,
    unsigned char * pucAdr
)
{
    int ia;
    int iFrame;
    int iBlock;
    int iAbuf[1000];
    int iKer;
    int iNsampno;
/*     int iii; */
    unsigned short uhChanno;
    for (ia=0; ia<8; ia++) {
    }
    pucAdr += 8;
    memmove(&iFrame, pucAdr, 4);
    swap4b((unsigned int *)&iFrame);
    pucAdr += 4;
    memmove(&iBlock, pucAdr, 4);
    swap4b((unsigned int *)&iBlock);
    pucAdr += 4;
    pucAdr++;
    pucAdr++;
    iKer = win2fix(                                /* �����ͥ�ǡ��������Х��ȿ� */
        pucAdr,              /* ( I ) �����ͥ�ǡ���
                                         *      �ʥ����ͥ��ֹ椫��� */
        iAbuf,                        /* ( O ) ����ץ�ǡ��� */
        &uhChanno,          /* ( O ) �����ͥ��ֹ� */
        &iNsampno                      /* ( O ) ����ץ�󥰿� */
    );
    for (ia=0; ia<iNsampno; ia++) {
    }
}

#ifndef APE_PROT___H
#define APE_PROT___H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h>
#include <fcntl.h>

#ifdef DOS
#else
#include <unistd.h>
#endif

#include <v3win32_type.h>
#include <v3win32_define.h>

extern int
winget_chnl(
    unsigned char *pucPtr,              /* ( I ) �����ͥ�ǡ��� �ʥ�
                                         * ���ͥ��ֹ椫��� */
    unsigned short *puhSys_ch,          /* ( O ) �����ͥ��ֹ� */
    int *piOffsize,                     /* ( O ) ����ץ륵����(0---4) */
    int *piNsampno,                     /* ( O ) ����ץ�󥰿� */
    int *piAllbyte                      /* ( O ) ���Х��ȿ� * */
);

extern void usage(void);

extern int
read_write(
    FILE * psFile_in,
    FILE * psFile_out
);

extern int maxalloc(
    void **ppvPtr,    /** (I/O) �ݥ��� **/
    int   iAllbyte,   /** ( I ) alloc����Х��ȿ� **/
    int  *piMaxbyte   /** ( I ) ���ߤΥХ��ȿ� **/
);

extern void w32las_(
    char * pcFilenow,        /** ( O ) ���ߤΥե�����̾ **/
    char * pcLast3,          /** ( O ) �Ǹ夫�飳���ܤΥǡ���̾ **/
    int  * piRet             /** ( O ) �꥿���󥳡���(= 0 ���!= 0 �۾ｪλ) **/
);

extern void w32nxt_(
    char * pcFilenow,        /** ( I ) ���ߤΥǡ����ե�����̾ **/
    char * pcFileend,        /** ( I ) ����ɻ���ǡ����ե�����̾ **/
    char * pcFilenext,       /** ( O ) ���Υǡ����ե�����̾ **/
    int  * piRet             /** ( O ) �꥿���󥳡���(= 0 ���!= 0 �۾ｪλ) **/
);

extern int w32cmpdata(
    WIN32_DATA * pstData1,
    WIN32_DATA * pstData2
);

extern void w32dir_(
    char * pcFilename,       /** ( I ) �ե�����̾(����ʸ�������եե�����̾) **/
    char * pcFiledir,        /** ( I ) �ǥ��쥯�ȥ꡼̾ **/
    int * piRet
);
extern void thrini_(
    int * piPid1,  /** ( O ) �ץ����ɣġ�END�Ԥ��� **/
    int * piPid2   /** ( O ) �ץ����ɣġʿƥץ����ƻ��ѡ� **/
);
extern void setglb_(
    char * pcEnv           /** ( I ) �ǡ�����¸�ߤ���ǥ��쥯�ȥ꡼ **/
);
extern void setgl2_(
    char * pcEnv           /** ( I ) �ǡ�����¸�ߤ���ǥ��쥯�ȥ꡼ **/
);
extern void thrwat_(
    int * piPid,
    int * piIstat,
    int * piRet
);
extern void bytrev_(unsigned char * puc1, int * piByte);
extern void lastdt_(
    char * pcLast3,          /** ( O ) �Ǹ夫�飳���ܤΥǡ���̾ **/
    int  * piRet             /** ( O ) �꥿���󥳡���(= 0 ���!= 0 �۾ｪλ) **/
);
extern void bitmov_(
    unsigned char * pucTo,       /** ( O ) ��ư��ΥХ��ȥ��ꥢ **/
    int           * piBitadrTo,  /** ( I ) pucTo����Ƭ����Υӥåȥ��ɥ쥹(���ޤ��ϣ����ܿ�) **/
    unsigned char * pucFr,       /** ( I ) ��ư���ΥХ��ȥ��ꥢ **/
    int           * piBitadrFr,  /** ( I ) pucFr����Ƭ����Υӥåȥ��ɥ쥹(���ޤ��ϣ����ܿ�) **/
    int           * piBitnum     /** ( I ) ��ư����ӥåȿ�(�����ܿ�) **/
);
extern void w32ums_(
    int  * piMode,   /** ( I ) ���ꤹ��ޥ����� **/
    int  * piOld     /** ( O ) ����ޤǤΥޥ����� **/
);
extern void w32mkd_(
    char * pcPath,
    int  * piMode
);
extern int w32cmp( char * pcFile1, char * pcFile2);
extern void bit4mv_(
    unsigned char * pucTo,      /** ( O ) char of To **/
    int           * piBitadrTo,  /** ( I ) pucTo�Υӥåȥ��ɥ쥹(���ޤ��ϣ����ܿ�) **/
    unsigned char * pucFr,      /** ( I ) char of From **/
    int           * piBitadrFr   /** ( I ) pucFr�Υӥåȥ��ɥ쥹(���ޤ��ϣ����ܿ�) **/
);
extern int date32_(
    char * pcDate1,
    char * pcDate2,
    size_t  * piNum
);
extern void w32upp_(
    char * pcFilestart,      /** ( I ) ���ߤΥǡ����ե�����̾ **/
    char * pcFileend,        /** ( I ) ����ɻ���ǡ����ե�����̾ **/
    char * pcFilenext,       /** ( O ) ���Υǡ����ե�����̾ **/
    int  * piRet             /** ( O ) �꥿���󥳡���(= 0 ���!= 0 �۾ｪλ) **/
);
extern void w32nxt_(
    char * pcFilenow,        /** ( I ) ���ߤΥǡ����ե�����̾ **/
    char * pcFileend,        /** ( I ) ����ɻ���ǡ����ե�����̾ **/
    char * pcFilenext,       /** ( O ) ���Υǡ����ե�����̾ **/
    int  * piRet             /** ( O ) �꥿���󥳡���(= 0 ���!= 0 �۾ｪλ) **/
);
extern void w32fnm_(
    char * pcFilenow,        /** ( I ) ���ߤΥǡ����ե�����̾ **/
    int  * piKbegin,         /** ( I ) ���Υǡ����ե�����̾�ε����
                              **       1:̵���˺ǽ�Υǡ����ե��������Ф�
                              **       2:pcFilenow����礭���������������
                              **       3:pcFilenow��꾮�����������������
                              **       4:̵���˺Ǹ�Υǡ����ե��������Ф�
                              **       ����¾:pcFilenow�μ��Τ��
                              **/
    char * pcFilenext,       /** ( O ) �ǡ����ե�����̾ **/
    int * piRet              /** ( O ) �꥿���󥳡���(= 0 ���!= 0 �۾ｪλ) **/
);
extern void win32read_(
    int * piStart,           /** ( I ) ��������ץ�(1:YES, 0:NO) **/
    char * pcFilestart,      /** ( I ) ��������ץ󤹤�ե�����̾(����ʸ�������եե�����̾) **/
    char * pcFileend,        /** ( I ) �Ǹ�Υե�����̾(����ʸ�������եե�����̾) **/
    int  * piRet             /** ( O ) �꥿���󥳡���(0:���1:�ǡ�����λ��999:�۾ｪλ) **/
);
extern void w32dwn_(
    char * pcFilestart,      /** ( I ) ���ߤΥǡ����ե�����̾ **/
    char * pcFileend,        /** ( I ) ����ɻ���ǡ����ե�����̾ **/
    char * pcFilenext,       /** ( O ) ���Υǡ����ե�����̾ **/
    int  * piRet             /** ( O ) �꥿���󥳡���(= 0 ���!= 0 �۾ｪλ) **/

);
extern void w32ls1_(
    char * pcFilenow,        /** ( I ) ���ߤΥǡ����ե�����̾ **/
    int * piRet              /** ( O ) �꥿���󥳡���(= 0 ���!= 0 �۾ｪλ) **/
);

extern void swap4b(unsigned int *pic);
extern void swap2b(unsigned short int *pic);
extern void bit4mv_(
    unsigned char * pucTo,        /** ( O ) char of To **/
    int           * piBitadrTo,   /** ( I ) pucTo�Υӥåȥ��ɥ쥹(���ޤ��ϣ����ܿ�) **/
    unsigned char * pucFr,        /** ( I ) char of From **/
    int           * piBitadrFr    /** ( I ) pucFr�Υӥåȥ��ɥ쥹(���ޤ��ϣ����ܿ�) **/
);


#endif

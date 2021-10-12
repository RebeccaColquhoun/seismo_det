#ifndef C20_PROT__HHH
#define C20_PROT__HHH

#include <s8c32_type.h>

extern int c32dataread_write(
    int           iKbeginfile,     /** ( I ) �ǽ�Υե����뤫 **/
    char        * pcFilename_out,  /** ( I ) �ɤ߹���ףɣΣ����ǡ����ե�����̾ **/
    char        * pcFilename_in,   /** ( I ) �ɤ߹���ףɣΣ����ǡ����ե�����̾ **/
    int         *piHandle_out,
    int         *piHandle_in
);

extern void c32realloc(
    C32_HEADER **pptHeader,    /** (I/O) �إå����Υݥ��󥿡� **/
    int          iNheader      /** ( I ) ���ݤ���إå����θĿ� **/
);

extern void c32dataread(
    unsigned char   ucTop[4],      /** (I/O) �ե��������Ƭ���Х��� **/
    C32_HEADER ** pptC32header,    /** (I/O) �إå�����ʬ�Υݥ��󥿡� **/
    int         * piNchannel,       /** (I/O) �������ͥ�θĿ�(�إå����θĿ�) **/
    int           iHandle_temp,    /** ( I ) �ƥ�ݥ�꡼�ե�����Υϥ�ɥ� **/
#ifdef MINGW
    int         * ptCurpos,        /** (I/O) �ƥ�ݥ�꡼�ե����륫���ȥݥ������ **/
#else
    off_t       * ptCurpos,        /** (I/O) �ƥ�ݥ�꡼�ե����륫���ȥݥ������ **/
#endif
    char        * pcFilename       /** ( I ) �ɤ߹���ףɣΣ����ǡ����ե�����̾ **/
);

extern void ftime_(int * iTime);

extern void bytrev_(unsigned char * puc1, int * piByte);

extern void bitmov_(
    unsigned char * pucTo,       /** ( O ) ��ư��ΥХ��ȥ��ꥢ **/
    int           * piBitadrTo,  /** ( I ) pucTo����Ƭ����Υӥåȥ��ɥ쥹(���ޤ��ϣ����ܿ�) **/
    unsigned char * pucFr,       /** ( I ) ��ư���ΥХ��ȥ��ꥢ **/
    int           * piBitadrFr,  /** ( I ) pucFr����Ƭ����Υӥåȥ��ɥ쥹(���ޤ��ϣ����ܿ�) **/
    int           * piBitnum     /** ( I ) ��ư����ӥåȿ�(�����ܿ�) **/
);

extern void bit4mv_(
    unsigned char * pucTo,      /** ( O ) char of To **/
    int           * piBitadrTo,  /** ( I ) pucTo�Υӥåȥ��ɥ쥹(���ޤ��ϣ����ܿ�) **/
    unsigned char * pucFr,      /** ( I ) char of From **/
    int           * piBitadrFr   /** ( I ) pucFr�Υӥåȥ��ɥ쥹(���ޤ��ϣ����ܿ�) **/
);

extern void c32datawrite(
    unsigned char ucTop[4],        /** (I/O) �ե��������Ƭ���Х��� **/
    C32_HEADER ** pptC32header,    /** (I/O) �إå�����ʬ�Υݥ��󥿡� **/
    int         * piNchannel,      /** (I/O) �������ͥ�θĿ�(�إå����θĿ�) **/
    int           iHandle_temp,    /** ( I ) �ƥ�ݥ�꡼�ե�����Υϥ�ɥ� **/
    char        * pcFilename,      /** ( I ) ���ϣףɣΣ����ǡ����ե�����̾ **/
    WIDECHAN    *puiAll_channel,   /** ( I ) ���ǡ�����¸�ߤ�������ͥ�
                                         **       Ʊ����Τϡ��Ϥ֤��Ƥ��� **/
    int iNall_channel                   /** ( I ) ���ǡ�����¸�ߤ�������ͥ�����
                                         **       puiAll_channel�θĿ� **/

);

extern void c32datasort(
    C32_HEADER ** pptC32header,            /** (I/O) �إå�����ʬ�Υݥ��󥿡� **/
    int         * piNchannel,              /** (I/O) �������ͥ�إå����θĿ� **/
    WIDECHAN **ppuiAll_channel,            /** ( O ) ���ǡ�����¸�ߤ�������ͥ�
                                            **       Ʊ����Τϡ��Ϥ֤��Ƥ��� **/
    int *piNall_channel                    /** ( O ) ���ǡ�����¸�ߤ�������ͥ�����
                                            **       **ppuiAll_channel�θĿ� **/
);
extern int c32cmp1(
    C32_HEADER * pstData1,
    C32_HEADER * pstData2
);

extern void c32usage(void);
extern int maxalloc(
    void **ppvPtr,    /** (I/O) �ݥ��� **/
    int   iAllbyte,   /** ( I ) alloc����Х��ȿ� **/
    int  *piMaxbyte   /** ( I ) ���ߤΥХ��ȿ� **/
);
extern int c32cmp2(
    WIDECHAN * pstData1,
    WIDECHAN * pstData2
);
extern int
winget_chnl(
    unsigned char *pucPtr,              /* ( I ) �����ͥ�ǡ��� �ʥ�
                                         * ���ͥ��ֹ椫��� */
    unsigned short *puhSys_ch,          /* ( O ) �����ͥ��ֹ� */
    int *piOffsize,                     /* ( O ) ����ץ륵����(0---4) */
    int *piNsampno,                     /* ( O ) ����ץ�󥰿� */
    int *piAllbyte                      /* ( O ) ���Х��ȿ� * */
);
extern void swap4b(unsigned int *pic);
extern void swap2b(unsigned short int *pic);


#endif  /** C20_PROT__HHH **/

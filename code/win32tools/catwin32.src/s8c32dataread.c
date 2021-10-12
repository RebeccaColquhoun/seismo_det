#ifdef MINGW
/* #undef _INC_FCNTL */
#include <fcntl.h>
#include <io.h>
#if 0
#define O_RDONLY       0x0000  /* open for reading only */
#define O_WRONLY       0x0001  /* open for writing only */
#define O_RDWR         0x0002  /* open for reading and writing */
#define O_APPEND       0x0008  /* writes done at eof */
#define O_CREAT        0x0100  /* create and open file */
#define O_TRUNC        0x0200  /* open and truncate */
#define O_EXCL         0x0400  /* open only if file doesn't already exist */
#define O_TEXT         0x4000  /* file mode is text (translated) */
#define O_BINARY       0x8000  /* file mode is binary (untranslated) */
#endif
#endif
#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <s8c32_type.h>
#include <s8c32_prot.h>
#define MAXBYTE 5000000
extern int igTest;
void c32dataread(
    unsigned char ucTop[4],        /** (I/O) �ե��������Ƭ���Х��� **/
    C32_HEADER ** pptC32header,    /** (I/O) �إå�����ʬ�Υݥ��󥿡� **/
    int         * piNchannel,      /** (I/O) �������ͥ�θĿ�(�إå����θĿ�) **/
    int           iHandle_temp,    /** ( I ) �ƥ�ݥ�꡼�ե�����Υϥ�ɥ� **/
#ifdef MINGW
    int         * ptCurpos,        /** (I/O) �ƥ�ݥ�꡼�ե����륫���ȥݥ������ **/
#else
    off_t       * ptCurpos,        /** (I/O) �ƥ�ݥ�꡼�ե����륫���ȥݥ������ **/
#endif
    char        * pcFilename       /** ( I ) �ɤ߹���ףɣΣ����ǡ����ե�����̾ **/
)
{
    int iOffsize;
    int iNsampno;
    unsigned char ucSampdate[8];   /** ����ץ�󥰳���ǯ������ʬ�� **/
    int iHandle;
    size_t iSsize ;                
    unsigned char ucDat_w[4];
    static unsigned char * pucDat = NULL;
    int ia;
    int iReadbyte;
    unsigned char uc1;
    unsigned char uc2;
    unsigned short int uhChanno0;
    unsigned short int uhChanno;
    int iDate[8];
    int iNframe;
    int iBsize;
    int iAdrbit;
    int iAdrbyte;
    int iAllbit;
    int iAllbyte;
    int iSize;
    int iAdrbit_head;
    int iAdrbyte_head;
#ifdef MINGW
    int result;
#endif
fprintf(stderr, "%s\n", pcFilename);
    if (strcmp(pcFilename, "-") == 0) {
        iHandle = 0;                       /** ɸ������ **/
#ifdef MINGW
       /* "stdin" ��Х��ʥ� �⡼�ɤ����ꤷ�ޤ��� */
        result=_setmode(_fileno(stdin),_O_BINARY);
        if( result == -1 ) {
            fprintf(stderr, "***** ERROR ***** The mode does not set.(%s %d)\n",
                    __FILE__, __LINE__);
           exit(0);
        }
#endif
    } else {
#ifdef MINGW
        iHandle = open(pcFilename, O_RDONLY|O_BINARY );
#else
        iHandle = open(pcFilename, O_RDONLY );
#endif
        if ( iHandle == -1 ) {
            fprintf (stderr, "***** ERROR ***** File open error.(%s)(c32dataread)\n", pcFilename ) ;
            goto ret;
        }
    }
    iReadbyte = 0;
    /* �ȥåץǡ��� */
    iSsize = read ( iHandle , ucDat_w , (size_t) 4 ) ;
    if ( iSsize != 4 ) {
        fprintf (stderr, "***** ERROR ***** File read error.(%s)(c32dataread)\n", pcFilename ) ;
        goto ret2;
    }
    iReadbyte += 4;
    if (ucTop[0] == 255 && ucTop[1] == 255 && ucTop[2] == 255 && ucTop[3] == 255) {
        ucTop[0] = ucDat_w[0];
        ucTop[1] = ucDat_w[1];
        ucTop[2] = ucDat_w[2];
        ucTop[3] = ucDat_w[3];
    } else {
        if (ucTop[0] != ucDat_w[0] || ucTop[1] != ucDat_w[1] || ucTop[2] != ucDat_w[2] || ucTop[3] != ucDat_w[3]) {
            fprintf(stderr, "***** WARNING ***** The file top data is differrent from first win32 data.(c32dataread)\n");
        }
    }
    while (1) {
        iSsize = read ( iHandle , ucSampdate , (size_t) 8 ) ;
                                                 /** ����ץ�󥰳���ǯ������ʬ�å꡼�� **/
        if ( iSsize != 8 ) goto ret2;            /** ��λ **/
        for (ia=0; ia<8; ia++) {
            uc1= ucSampdate[ia] & 0xf0;
            uc1 = uc1 >> 4;
            uc2= ucSampdate[ia] & 0x0f;
            iDate[ia]=uc1*10+uc2;
        }
        iReadbyte += 8;
#if 0
fprintf(stderr, "%02d%02d%02d%02d%02d%02d(%02d)\n",
                           iDate[1], iDate[2], iDate[3],
                           iDate[4], iDate[5], iDate[6], iDate[7]);
#endif
        if(iDate[7] != 0) {
            fprintf(stderr,
              "***** ERROR ***** The sampling time error.(lower decimal point = %02d)(c32dataread)\n", iDate[7]);
            goto ret2;
        }
        iSsize = read ( iHandle , &iNframe , (size_t) 4 ) ; 
                                                 /** �ե졼�����Ĺ�꡼�� **/
        if ( iSsize != 4 ) goto ret2;
/*         bytrev_((unsigned char *)&iNframe, (int *)(&i04)); */
        swap4b((unsigned int *)&iNframe);
        iReadbyte += 4;
        iSsize = read ( iHandle , &iBsize , (size_t) 4 ) ;
        if ( iSsize != 4 ) goto ret2;
/*         bytrev_((unsigned char *)&iBsize, (int *)(&i04)); */
        swap4b((unsigned int *)&iBsize);
        if (iBsize >= MAXBYTE) {
            fprintf(stderr, "***** ERROR ***** The data block length is over maximum. (%d)(c32dataread)\n", MAXBYTE);
            exit (0);
        }
        iReadbyte += 4;
        /** �����ͥ�֥�å����� **/
        if(pucDat != NULL) free(pucDat);
        pucDat = malloc((size_t)iBsize);
        if (pucDat == NULL) {
            fprintf(stderr, "***** ERROR ***** Memory alloc error.(%s %d)\n",
                    __FILE__, __LINE__);
           exit(0);
        }
        iSsize = read  (iHandle, pucDat, (size_t)iBsize);
        if ( iSsize != (size_t)iBsize ) goto ret2;
        iReadbyte += iBsize;
        iAdrbit = 0;  /** ��Ƭ����Υӥåȥ��ɥ쥹 **/
        iAdrbyte = 0;
/*         while(iAdrbit+32 < iBsize*8) { */
        while(iAdrbyte+4 < iBsize) {
            iAdrbit = ((iAdrbit+7)/8)*8;        /** �Х��ȶ����ˤ��� **/
            iAdrbit_head = iAdrbit ;            /** �ȿ��ɣ� �ӥåȰ��� **/
            iAdrbyte_head = iAdrbyte;
            /** �ȿ��ɣ� ̵�� **/
/*             bitmov_((unsigned char *)&ucId1, &ii0,&pucDat[0], &iAdrbit, &ii8); */
            iAdrbit += 8;
            iAdrbyte += 1;
            /** �ȿ����֣ɣ� ̵�� **/
            iAdrbit += 8;
            iAdrbyte += 1;
            memmove(&uhChanno0, &pucDat[iAdrbyte-2], 2);
            swap2b((unsigned short int *)&uhChanno0);
/*             if (igTest == 2) { */
/*                 uhChanno0 = 0x0809; */
/*                 memmove(&pucDat[iAdrbyte-2], &uhChanno0, 2); */
/*             } */
            winget_chnl(
                &pucDat[iAdrbyte],              /* ( I ) �����ͥ�ǡ��� �ʥ�
                                                 * ���ͥ��ֹ椫��� */
                &uhChanno,          /* ( O ) �����ͥ��ֹ� */
                &iOffsize,                     /* ( O ) ����ץ륵����(0---4) */
                &iNsampno,                     /* ( O ) ����ץ�󥰿� */
                &iAllbyte                      /* ( O ) ���Х��ȿ� * */
            );
            iAdrbit += iAllbyte*8;
            iAdrbyte += iAllbyte;
            iAllbit = iAdrbit - iAdrbit_head ;
            iAllbyte = iAdrbyte-iAdrbyte_head;
            (*piNchannel)++;
            c32realloc(pptC32header, *piNchannel);
            for (ia=0; ia<8; ia++) {
                (*pptC32header+(*piNchannel-1))->ucStart[ia]=ucSampdate[ia];
            }
            (*pptC32header+(*piNchannel-1))->iNframe = iNframe;
/*             bytrev_((unsigned char *)&uhChanno, (int *)(&i02)); */
/*             swap2b((unsigned short int *)&uhChanno); */
            (*pptC32header+(*piNchannel-1))->uhChanno0 = uhChanno0;
            (*pptC32header+(*piNchannel-1))->uhChanno = uhChanno;
            (*pptC32header+(*piNchannel-1))->tOffset = *ptCurpos;
            (*pptC32header+(*piNchannel-1))->iByte = iAllbyte;
/* fprintf(stderr, "s8c32dataread iByte=%d\n", iAllbyte); */
            iSize = write ( iHandle_temp , &pucDat[iAdrbyte_head] , iAllbyte ) ;
            if ( iSize != iAllbyte ) {
                fprintf(stderr, "***** ERROR ***** The temporary file write error.(c32dataread)\n");
                goto ret2;
            }
            *ptCurpos += iAllbyte ;
        }
    }  /** while (1) **/
ret2:;
    if (iHandle != 0) close(iHandle);  /** ɸ�����ϤǤʤ���Х����� **/
ret:;
    if(pucDat != NULL) {
        free(pucDat);
        pucDat = NULL;
    }
}

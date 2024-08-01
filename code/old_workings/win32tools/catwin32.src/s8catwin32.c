#ifdef MINGW
/* #undef _INC_FCNTL */
#include <fcntl.h>
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
#include <string.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <s8c32_type.h>
#include <s8c32_prot.h>
int igTest;
int main(
    int iArgc,
    char ** ppArgv
)
{
    int             iKbeginfile;
    int             iKer;
    int             iHandle_out;
    int             iHandle_in;
/*  char           *pcTmp ;       */             /*  �ƥ�ݥ�꡼�ե�����̾ */
    char            cTempfile[1024];             /*  �ƥ�ݥ�꡼�ե�����̾ */
#ifdef MINGW
    int             tCurpos;
#else
    off_t           tCurpos;
#endif
    int             ia;
    int             iTimes[7];                   /* ���߻��� */
    int             iTimee[7];                   /* ���߻��� */
    int             iHandle_temp = 0;            /* �ե�����ϥ�ɥ� */
    int             iNchannel;
    C32_HEADER  *   ptC32header;                 /* �إå�����ʬ�Υݥ��󥿡� */
    unsigned char   ucTop[4];                    /* �ե��������Ƭ���Х��� */
    char            cFilename_out[1024];             /* ���ϣףɣΣ����ǡ����ե�����̾ */
    int             iKargv[10000];               /* ���ѺѤߥե饰 */
    int             iCount;                      /* �����󥿡� */
    int             iKsort;                      /* ���諒���ȥե饰 */
    int             iKusage;                     /* ������ˡɽ���ե饰 */
    WIDECHAN * puiAll_channel;         /** ���ǡ�����¸�ߤ�������ͥ�
                                                  ** Ʊ����Τϡ��Ϥ֤��Ƥ��� **/
    int             iNall_channel;               /** ���ǡ�����¸�ߤ�������ͥ�����
                                                  ** puiAll_channel�θĿ� **/
#ifdef MINGW
    int result;
    char * psTemp;
#endif
    ftime_(iTimes);
    fprintf(stderr,"----- catwin32_32 start %4d/%02d/%02dT%02d:%02d:%02d -----\n",
           iTimes[0],iTimes[1],iTimes[2],iTimes[3],iTimes[4],iTimes[5]);
    cTempfile[0] = '\0';
    for (ia=0; ia<10000; ia++) {
        iKargv[ia] = 0;
    }
    /** -h -? ���ץ��������å� **/
    iKusage = 0;
    for (ia=1; ia<iArgc; ia++) {
        if (strncmp(*(ppArgv+ia), "-h", 2) == 0 ||
            strncmp(*(ppArgv+ia), "-H", 2) == 0 ||
            strncmp(*(ppArgv+ia), "-?", 2) == 0) {
            iKusage = 1;
            iKargv[ia] = 1;
            break;
        }
    }
    /** ������ˡ�ץ��ȡ� **/
    if (iKusage == 1) {
        c32usage();
        exit (0);
    }
    /** -s ���ץ��������å�(SORT) **/
    iKsort = 0;
    for (ia=1; ia<iArgc; ia++) {
        if (strncmp(*(ppArgv+ia), "-s", 2) == 0 ||
            strncmp(*(ppArgv+ia), "-S", 2) == 0) {
            iKsort = 1;
            iKargv[ia] = 1;
            break;
        }
    }
    /** -o ���ץ��������å� **/
    cFilename_out[0] = '\0';                          /* �Σգ̣̤ξ��Ͻ��ϥե��������ʤ� */
    for (ia=1; ia<iArgc; ia++) {
        if (strncmp(*(ppArgv+ia), "-o", 2) == 0 ||
            strncmp(*(ppArgv+ia), "-O", 2) == 0) {
            iKargv[ia] = 1;
            if (strlen(*(ppArgv+ia)) <= 2) {
                if (ia+1 < iArgc) {
                    strcpy(cFilename_out, *(ppArgv+ia+1));
                    iKargv[ia+1] = 1;
                }
            } else {
                strcpy(cFilename_out, *(ppArgv+ia)+2);
            }
            break;
        }
    }
    if (iKsort == 0) {
        iKbeginfile = 1;
        iCount = 0;
        for (ia=1; ia<iArgc; ia++) {
            if (iKargv[ia] == 1) continue;
            iCount++;
        }
        if (iCount == 0) {
            iKer = c32dataread_write(iKbeginfile, cFilename_out, "-", &iHandle_out, &iHandle_in);
            if(iKer) goto ret;
        } else {
            for (ia=1; ia<iArgc; ia++) {
                if (iKargv[ia] == 1) continue;
                igTest = ia;
                iKer = c32dataread_write(iKbeginfile, cFilename_out, *(ppArgv+ia),
                       &iHandle_out, &iHandle_in);
                if(iKer) goto ret;
                iKbeginfile = 0;
            }
            
        }
        if (iHandle_out != 1) close(iHandle_out);
        goto ret;
    }
    /** �ƥ�ݥ�꡼�ե����륪���ץ� **/
    strcpy(cTempfile, "tmp.catwin32.XXXXXX");
#ifdef MINGW
    psTemp = mktemp(cTempfile);
    if ( psTemp == (char *)NULL ) {
        fprintf (stderr, "***** ERROR ***** File open error.(%s)(%s %d)\n",
                         psTemp, __FILE__, __LINE__ ) ;
        goto ret;
    }
    iHandle_temp = open(psTemp, O_RDWR|O_CREAT|O_BINARY,0666 );
    if ( iHandle_temp == -1 ) {
        fprintf (stderr, "***** ERROR ***** File open error.(%s)(%s %d)\n",
                         psTemp, __FILE__, __LINE__ ) ;
        goto ret;
    }
#else
    iHandle_temp = mkstemp(cTempfile);
#endif /* ifdef MINGW */
    if ( iHandle_temp == -1 ) {
        fprintf (stderr, " The temporary file open error.(catwin32)\n" ) ;
        exit ( 0 ) ;
    }
#ifdef MINGW
       /* "iHandle_temp" ��Х��ʥ� �⡼�ɤ����ꤷ�ޤ��� */
        result = _setmode( iHandle_temp, O_BINARY );
        if( result == -1 ) {
            fprintf(stderr, "***** ERROR ***** I could not set the mode.(%s %d)\n",
                    __FILE__, __LINE__);
           exit(0);
        }
#endif
    tCurpos = 0;                             /* ����ե����륫���ȥݥ������ */
    iNchannel = 0;                           /* �Ŀ������å� */
    ptC32header = NULL;                      /* �ݥ��󥿡�NULL���å� */
    ucTop[0]=255;                            /* �ե��������Ƭ���Х��� */
    ucTop[1]=255;
    ucTop[2]=255;
    ucTop[3]=255;
    iCount = 0;
    for (ia=1; ia<iArgc; ia++) {
        if (iKargv[ia] == 1) continue;
        iCount++;
    }
    if (iCount == 0) {
        c32dataread(ucTop,&ptC32header, &iNchannel, iHandle_temp, &tCurpos, "-" ) ;
    } else {
        for (ia=1; ia<iArgc; ia++) {
            if (iKargv[ia] == 1) continue;
/* fprintf(stderr,"------ %s ---------- %d=%d\n", *(ppArgv+ia), ia, iKargv[ia]); */
            igTest = ia;
            c32dataread(ucTop,&ptC32header, &iNchannel, iHandle_temp, &tCurpos, *(ppArgv+ia) ) ;
        }
    }
    if (iKsort == 1) {       /** �����Ȥ��뤫 **/
        c32datasort(
            &ptC32header,    /** (I/O) �إå�����ʬ�Υݥ��󥿡� **/
            &iNchannel,      /** (I/O) �������ͥ�θĿ�(�إå����θĿ�) **/
            &puiAll_channel, /** ( O ) ���ǡ�����¸�ߤ�������ͥ�
                              **       Ʊ����Τϡ��Ϥ֤��Ƥ��� **/
            &iNall_channel   /** ( O ) ���ǡ�����¸�ߤ�������ͥ�����
                              **       *puiAll_channel�θĿ� **/
        );
    }
    c32datawrite(
        ucTop,           /** (I/O) �ե��������Ƭ���Х��� **/
        &ptC32header,    /** (I/O) �إå�����ʬ�Υݥ��󥿡� **/
        &iNchannel,      /** (I/O) �������ͥ�θĿ�(�إå����θĿ�) **/
        iHandle_temp,    /** ( I ) �ƥ�ݥ�꡼�ե�����Υϥ�ɥ� **/
        cFilename_out,   /** ( I ) ���ϣףɣΣ����ǡ����ե�����̾ **/
        puiAll_channel,  /** ( I ) ���ǡ�����¸�ߤ�������ͥ�
                          **       Ʊ����Τϡ��Ϥ֤��Ƥ��� **/
        iNall_channel    /** ( I ) ���ǡ�����¸�ߤ�������ͥ�����
                          **       puiAll_channel�θĿ� **/
    );
ret:;
    if (cTempfile[0] != '\0') {
        close ( iHandle_temp ) ;
        unlink ( cTempfile ) ;
    }
    ftime_(iTimee);
    fprintf(stderr, "----- catwin32_32 start %4d/%02d/%02dT%02d:%02d:%02d -----\n",
           iTimes[0],iTimes[1],iTimes[2],iTimes[3],iTimes[4],iTimes[5]);
    fprintf(stderr, "----- catwin32_32  end  %4d/%02d/%02dT%02d:%02d:%02d -----\n",
           iTimee[0],iTimee[1],iTimee[2],iTimee[3],iTimee[4],iTimee[5]);
    exit (0);
}

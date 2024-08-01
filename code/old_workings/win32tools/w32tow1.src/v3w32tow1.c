#include <v3win32_type.h>
#include <v3win32_prot.h>
/* #include <ape_define.h> */
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#define MAXBYTE 10000000
extern int getopt(int argc, char * const argv[], const char *optstring);
typedef union __UNION_VAR
{
    void * pv;
    WIN32_DATA * pst32;
} UNION_VAR;
/** WIN32�ե������WIN1�ե�������Ѵ����� **/
int main(
    int iArgc,
    char ** ppcArgv
)
{
    int iOffsize;
    int iSampno;
    int iAllchbyte;
    int iKsort;
    int iNwin32data;
/*     static WIN32_DATA *pstWin32data = NULL; */
    static UNION_VAR uni = {NULL};
    static int iMaxbyte = 0;
    int iNumchannel;
    int iKbegin;
    int iRet = 0;
    int iKdiff;
    int iKsame;
    int iKer;
    int iAllbyte;
    int iAllbyte_w;
    fpos_t iHeadpos;
    fpos_t iLastpos;
    int iWritebyte;
    int iWrite_start_byte;
    int iStart_byte;
    int iForm[4];
    int iFrlen;
    FILE * psFile_in;
    FILE * psFile_out;
/*     unsigned char ucDat[MAXBYTE]; */
    unsigned char *ucDat = NULL;
    unsigned char ucDat_date[8];
    size_t iCount;
    size_t iCount1;
    int    iBsize;
    int    iAdrbyte;
    int    ib;
    unsigned char uc1;
    unsigned char uc2;
    int iDate[8];
    unsigned short int uhChanno;
    char cFname_in[256];
    char cFname_out[256];
    int ia;
    int iNbyte;
    int c;
/*     extern char * optarg; */
    extern int optind;
    ucDat = (unsigned char *) malloc(sizeof(char)*MAXBYTE);
    if (ucDat == NULL) {
        printf("***** ERROR ***** The memory alloc error.(%s %d)\n", __FILE__, __LINE__);
        exit (0);
    }
    iNwin32data = 0;
    iKsort = 0;
    while ((c = getopt(iArgc, ppcArgv, "sShH?")) != EOF) {
        switch (c) {
        case 'S':
        case 's':
            iKsort = 1;
            break;
        case 'H':                       /* usage print */
        case 'h':                       /* usage print */
        case '?':                       /* usage print */
        default:
            usage();
            exit(1);
        }
    }
/*     printf("optind = %d iArgc = %d\n", optind, iArgc); */
    if (iArgc <= optind+1 || iArgc > optind+2) {
        usage();
        exit (1);
    }
/*    printf("ppcArgv[optind] = %s ppcArgv[optind+1] = %s\n", ppcArgv[optind], ppcArgv[optind+1] ); */
    strcpy(cFname_in, ppcArgv[optind]);
    psFile_in = fopen(cFname_in, "rb");
    if (psFile_in == NULL) {
        printf("***** ERROR ***** The %s file open error.\n", cFname_in);
        exit(1);
    }
    strcpy(cFname_out, ppcArgv[optind+1]);
    psFile_out = fopen(cFname_out, "wb");
    if (psFile_out == NULL) {
        printf("***** ERROR ***** The %s file open error.\n",cFname_out);
        exit (1);
    }
    /** �����Ȥ��ʤ���� **/
    if (iKsort == 0) {
        iKer = read_write(psFile_in, psFile_out);
        if (iKer) goto ret;
        goto ok;
    }
    /** �����Ȥ����� **/
    iCount = fread(ucDat, 1, 4, psFile_in);
    if (iCount != 4) {
        printf("***** ERROR ***** The %s file read error.\n",cFname_in);
        exit (1);
    }
    /**  �ե����ޥåȣɣġ��ե����ޥåȥС��������ꥶ���� **/
    for (ia=0; ia<4; ia++) {
        uc1= ucDat[ia] & 0xf0;
        uc1 = uc1 >> 4;
        uc2= ucDat[ia] & 0x0f;
        iForm[ia]=uc1*10+uc2;
    }
    if(iForm[0] != 0 || iForm[1] != 0 || iForm[2] != 0 || iForm[3] != 0) {
        printf("format id. or format version or reserve error.\n");
        printf("format id.=%02d, format version=%02d, reserve=%02d%02d\n",
            iForm[0], iForm[1], iForm[2], iForm[3]);
        exit (1);
    }
    /** ����ץ�󥰳���ǯ������ʬ�� **/
    while ((iCount1 = fread(&ucDat_date[0], 1, (size_t)8, psFile_in)) == 8) {
        for (ia=0; ia<8; ia++) {
            uc1= ucDat_date[ia] & 0xf0;
            uc1 = uc1 >> 4;
            uc2= ucDat_date[ia] & 0x0f;
            iDate[ia]=uc1*10+uc2;
        }
#if 0
    printf("%02d%02d%02d%02d%02d%02d(%02d)\n",
                       iDate[1], iDate[2], iDate[3],
                       iDate[4], iDate[5], iDate[6], iDate[7]);
#endif
        if(iDate[7] != 0) {
            printf("sampling time error.(lower decimal point = %02d)\n", iDate[7]);
            exit (1);
        }
        /** �ե졼�����Ĺ���� **/
        iCount1 = fread(&ucDat[12], 1, (size_t)4, psFile_in);
        if (iCount1 != 4) {
            printf("file read error2.\n");
            iRet = 999;
            goto ret;
        }
        memmove(&iFrlen, &ucDat[12], 4);
/*         bytrev_((unsigned char *)&iFrlen, (int *)(&i04)); */
        swap4b((unsigned int *)&iFrlen);
        if(iFrlen != 10) {
            printf("length of frame time error.(%d)\n", iFrlen);
            exit (1);
        }
        /** �ǡ����֥�å�Ĺ���� **/
        iCount1 = fread(&ucDat[16], 1, (size_t)4, psFile_in);
        if (iCount1 != 4) {
            printf("file read error2.\n");
            iRet = 999;
            goto ret;
        }
        memmove(&iBsize, &ucDat[16], 4);
/*         bytrev_((unsigned char *)&iBsize, (int *)(&i04)); */
        swap4b((unsigned int *)&iBsize);
        if (iBsize >= MAXBYTE) {
            printf("Data block length is over maximum. (%d)\n", MAXBYTE);
            exit (0);
        }
        /** �����ͥ�֥�å����� **/
        iCount1 = fread(ucDat, 1, (size_t)iBsize, psFile_in);
        if (iCount1 != iBsize) {
            printf("file read error2.\n");
            iRet = 999;
            goto ret;
        }
        iWritebyte = 0;
        iAdrbyte = 0;  /** ��Ƭ����ΥХ��ȥ��ɥ쥹 **/
        iNumchannel = 0;
        while(iAdrbyte+4 < iBsize) {
            /** �Х��ȶ����ˤ��� **/
            /** �ȿ��ɣ� ̵�� **/
            iAdrbyte += 1;
            /** �ȿ����֣ɣ� ̵�� **/
            iAdrbyte += 1;
            iWrite_start_byte = iAdrbyte;
            /** �����ͥ��ֹ������� **/
            iKer = winget_chnl(
                &ucDat[iAdrbyte],   /* ( I ) �����ͥ�ǡ��� �ʥ� 
                                     * ���ͥ��ֹ椫��� */
                &uhChanno,          /* ( O ) �����ͥ��ֹ� */
                &iOffsize,          /* ( O ) ����ץ륵����(0---4) */
                &iSampno,           /* ( O ) ����ץ�󥰿� */
                &iAllchbyte         /* ( O ) ���Х��ȿ� * */
            );
            iAdrbyte += iAllchbyte;
            iWritebyte = iAllchbyte;
            iNumchannel++;
            /** ���Υ����ͥ�ǡ�������꡼�˳�Ǽ **/
            iStart_byte = iWrite_start_byte;
            iNbyte = iWritebyte;
            iKer = maxalloc((void **)&uni.pv,
                         sizeof(WIN32_DATA)*(iNwin32data/10+1)*10, &iMaxbyte);
            if (iKer) {
                printf("***** ERROR ***** Memory alloc error.(%d)\n",
                                         (int)sizeof(WIN32_DATA)*(iNwin32data/10+1)*10);
                goto ret;
            }
            uni.pst32[iNwin32data].pucWindata = (unsigned char *)malloc((size_t)iNbyte);
            if (uni.pst32[iNwin32data].pucWindata == (unsigned char *)NULL) {
                printf("malloc error.\n");
                exit (1);
            }
            memmove(uni.pst32[iNwin32data].pucWindata, &ucDat[iStart_byte], (size_t)iNbyte);
            /** ���WIN1�ǡ�����񤭽Ф�����ξ���������꡼���ߤ��Ƥ��� **/
            uni.pst32[iNwin32data].iDate[0]=iDate[0];
            uni.pst32[iNwin32data].iDate[1]=iDate[1];
            uni.pst32[iNwin32data].iDate[2]=iDate[2];
            uni.pst32[iNwin32data].iDate[3]=iDate[3];
            uni.pst32[iNwin32data].iDate[4]=iDate[4];
            uni.pst32[iNwin32data].iDate[5]=iDate[5];
            uni.pst32[iNwin32data].iDate[6]=iDate[6];
            uni.pst32[iNwin32data].iDate[7]=iDate[7];
            uni.pst32[iNwin32data].ucDat_date[0]=ucDat_date[0];
            uni.pst32[iNwin32data].ucDat_date[1]=ucDat_date[1];
            uni.pst32[iNwin32data].ucDat_date[2]=ucDat_date[2];
            uni.pst32[iNwin32data].ucDat_date[3]=ucDat_date[3];
            uni.pst32[iNwin32data].ucDat_date[4]=ucDat_date[4];
            uni.pst32[iNwin32data].ucDat_date[5]=ucDat_date[5];
            uni.pst32[iNwin32data].ucDat_date[6]=ucDat_date[6];
            uni.pst32[iNwin32data].ucDat_date[7]=ucDat_date[7];
            uni.pst32[iNwin32data].iFrlen = iFrlen;
            uni.pst32[iNwin32data].uhChanno = uhChanno;
            uni.pst32[iNwin32data].iNbyte = iNbyte;
            /** �����ͥ��������ȥ��å� **/
            iNwin32data++;
        }
    }
    if (iNwin32data > 0) {
        /** �ߤ���줿�ǡ������äȥ����ͥ��ֹ�ǥ����� **/
        for (ia=0; ia<iNwin32data; ia++) {
            uni.pst32[ia].iSeq = ia;
        }
        qsort((void *) &uni.pst32[0], (size_t)iNwin32data,
                       sizeof(WIN32_DATA), (COMP) w32cmpdata);
         
        /** WIN1�ǡ�����񤭽Ф� **/
        fgetpos(psFile_out, &iHeadpos);
        fgetpos(psFile_out, &iLastpos);
        iAllbyte=0;
        for (ia=0; ia<iNwin32data; ia++) {
            iKbegin = 0;
            iKdiff = 0;
            if (ia != 0) {
                for (ib=0; ib<8; ib++) {
                    if (uni.pst32[ia-1].iDate[ib] != uni.pst32[ia].iDate[ib]) {
                        iKdiff = 1;
                        break;
                    }
                }
            }
            if(ia == 0 || (ia != 0 && iKdiff == 1)) {
                iAllbyte=0;
                iKbegin = 1;
                iHeadpos = iLastpos;
            }
            iAllbyte += uni.pst32[ia].iNbyte;
            if (ia != 0) {
                if (iKdiff == 0 &&
                    uni.pst32[ia-1].uhChanno == uni.pst32[ia].uhChanno) {
                    iKsame = 1;
                    if (uni.pst32[ia-1].iNbyte == uni.pst32[ia].iNbyte) {
                        for (ib=0; ib<uni.pst32[ia].iNbyte; ib++) {
                            if (uni.pst32[ia-1].pucWindata[ib] !=
                                uni.pst32[ia].pucWindata[ib]) {
                                iKsame = 0;
                                break;
                            }
                        }
                    } else {
                        iKsame = 0;
                    }
                    printf("***** Warning ***** Same channel no. exist. (%04x %02d%02d%02d%02d%02d%02d%02d%02d %d)\n",
                           uni.pst32[ia].uhChanno,
                           uni.pst32[ia].iDate[0],
                           uni.pst32[ia].iDate[1],
                           uni.pst32[ia].iDate[2],
                           uni.pst32[ia].iDate[3],
                           uni.pst32[ia].iDate[4],
                           uni.pst32[ia].iDate[5],
                           uni.pst32[ia].iDate[6],
                           uni.pst32[ia].iDate[7],
                           iKsame);
                }
            } /** if (ia != 0) **/
            /** �إå�����ʬ��񤭽Ф� **/
            fsetpos(psFile_out, &iHeadpos);
            iAllbyte_w = iAllbyte+10;
/*             bytrev_((unsigned char *)&iAllbyte_w, (int *)(&i04)); */
            swap4b((unsigned int *)&iAllbyte_w);
            iKer = fwrite(&iAllbyte_w, (size_t)4, (size_t)1, psFile_out);
            if (iKer != 1) {
                printf("file write error.\n");
                exit (1);
            }
            iKer = fwrite(&(uni.pst32[ia].ucDat_date[1]), (size_t)6, (size_t)1, psFile_out);
            if (iKer != 1) {
                printf("file write error.\n");
                exit (1);
            }
            /** �����ͥ�ǡ�����ʬ��񤭽Ф� **/
            if (iKbegin == 0) {
                fsetpos(psFile_out, &iLastpos);
            }
            iKer = fwrite(uni.pst32[ia].pucWindata, (size_t)uni.pst32[ia].iNbyte, (size_t)1, psFile_out);
            if (iKer != 1) {
                printf("file write error.\n");
                exit (1);
            }
            fgetpos(psFile_out, &iLastpos);
        }
        for (ia=0; ia<iNwin32data; ia++) {
            if (uni.pst32[ia].pucWindata == (unsigned char *)NULL) {
                printf("Pointer is NULL.\n");
                exit (1);
            }
            free((void *)uni.pst32[ia].pucWindata);
            uni.pst32[ia].pucWindata = (unsigned char *)NULL;
        }
        iNwin32data = 0;
    }
ok:;
    fclose(psFile_in);
    fclose(psFile_out);
    iRet = 0;
ret:;
    exit (0);
}

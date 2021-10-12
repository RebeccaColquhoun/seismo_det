#include <s4win2sac.h>
#include <stdio.h>
#include <string.h>
#define  TRUE 1
#define  FALSE 0
#define IQUAKE 40
/* #define MAX 1000000 */
#define MAX 2000000
extern float   gfRatio;
extern char gcBinext[50];
extern char gcAscext[50];
extern int     giKbinary;
extern int     giKascii;
extern _sac_header sac_header;
extern char sacfile[BUFSIZ];
extern float *yfunc;
extern char winfile[BUFSIZ];
extern char cDirname[1024];
extern char sunit[10];
extern int  giKendian;
extern unsigned char    gcOrganize1;
extern unsigned char    gcOrganize2;
extern int     giKwin32;
int     giKunit;
typedef union __UNION_VAR
{
    int  i;
    unsigned int ui;
    int l;
    unsigned int ul;
    float f;
    double d;
    short int h;
    unsigned short int uh;
    char c[4];
    char * pc;
} UNION_VAR;
extern int giKwidechan;
int 
win2sac0(int npts, int srate, unsigned int uiSysch, int *toptm)
{
    UNION_VAR uni;
    int    ii1;
    int    ii2;
    int    ii3;
    int    ia;
    char * pc1;
    char * pc2;
    char * pc3;
    int     iRet;
    int     iKer;
/*     float   fff; */
    float   o;
    float   evla;
    float   evlo;
    float   evdp;
    float   dist;
    float   az;
    float   a;
    float   t9;
    char    cUD[10];
    char    cUNE[MAX_SEIBUNCODE+1];
    int     i, sta;
    int     true, nzyear, nzjday, nzhour, nzmin, nzsec, nzmsec;
/*   int    nerr; */
    float   beg, del, cmpinc, cmpaz, stla, stlo, stel, sense;
/*   float  xdum; */
    char    cFsac_name[1024];
    char    cFbin_name[1024];
    char    cFasc_name[1024];
    char    kstnm[MAX_STATIONNAME+1], kcmp[MAX_SEIBUNCODE+1];
    int     yy, mm, dd, hor, min, sec;
    static FILE   *ptFile_sac = NULL;  /** サックファイルディスクリプター **/
    static FILE   *ptFile_bin = NULL;  /** バイナリーファイルディスクリプター **/
    static FILE   *ptFile_asc = NULL;  /** アスキーファイルディスクリプター **/
    true = TRUE;
    nzmsec = 0;
/* get SAC header information */
/* beginning value of time (sec of top time) */
/** modified by matsumura at 19991122 **/
    if (*toptm > 50) {
        yy = *toptm + 1900;
    } else {
        yy = *toptm + 2000;
    }
/*     printf("zzzzzzzzzzzzzzzzzzzzzzzzzzzz yy=%d\n", yy); */
    mm = *(toptm + 1);
    dd = *(toptm + 2);
    hor = *(toptm + 3);
    min = *(toptm + 4);
    sec = *(toptm + 5);
    nzyear = yy;
    nzjday = day_of_year(nzyear, mm, dd);
    nzhour = hor;
    nzmin = min;
    nzsec = sec;
    nzmsec = 0;
    beg = (float) sec;
    del = 1.0 / (float) srate;
    sta = stfind(uiSysch, kstnm, kcmp, &cmpaz, &cmpinc, &stla, &stlo, &stel, &sense);
    if (sta < 0) {
        if (giKwidechan == 0) {
            fprintf(stderr, "Channel No. %04x does not exist, exiting.\n", uiSysch);
        } else {
            fprintf(stderr, "Channel No. %08x does not exist, exiting.\n", uiSysch);
        }
        iRet = -1;
        goto ret;
    }
    giKunit = 0;
    if (strcmp(sunit, "m/s") == 0) {
        giKunit = 1;
    } else if (strcmp(sunit, "m/s/s") == 0) {
        giKunit = 2;
    } else if (strcmp(sunit, "rad") == 0) {
        giKunit = 3;
    }
    fprintf(stderr, "%s (%s); (%f,%f,%f) <%f;%f>\n",
        kstnm, kcmp, stla, stlo, stel, cmpaz, cmpinc);
    fprintf(stderr, "DATE = %4d/%3d  %2d:%2d:%2d\n",
        nzyear, nzjday, nzhour, nzmin, nzsec);
    if (giKwidechan == 0) {
        fprintf(stderr, "Channel No. = %04x\n", uiSysch);
    } else {
        fprintf(stderr, "Channel No. = %08x\n", uiSysch);
    }
/* output file name is from command line  04/14/98 S.OHMI */
    sprintf(cFsac_name, "%s%s.%s.%s", cDirname, kstnm, kcmp, sacfile);
    if (giKbinary == 1) {
        sprintf(cFbin_name, "%s%s.%s.%s", cDirname, kstnm, kcmp, gcBinext);
    }
    if (giKascii == 1) {
        sprintf(cFasc_name, "%s%s.%s.%s", cDirname, kstnm, kcmp, gcAscext);
    }
    fprintf(stderr, "npts = %d; beg = %f; dt = %f\n", npts, beg, del);
    fprintf(stderr, "Sensitivity = %e V/bit\n", sense);
    fprintf(stderr, "sacfile = %s\n", cFsac_name);
    if (giKbinary == 1) {
        fprintf(stderr, "binary file = %s\n", cFbin_name);
    }
    if (giKascii == 1) {
        fprintf(stderr, "ascii file = %s\n", cFasc_name);
    }
    for (i = 0; i < npts; i++) {
        if (giKunit == 1 || giKunit == 2) { /** m/s or m/s/s **/
            yfunc[i] = yfunc[i] * sense * 1000000000.0; /** nm/s or nm/s/s **/
        } else if (giKunit == 3) { /** rad **/
            yfunc[i] = yfunc[i] * sense * 1000000.0;  /** micro rad **/
        } else {
            yfunc[i] = yfunc[i] * sense;
        }
    }
    if (ptFile_sac != NULL) {
        fprintf(stderr, "SAC file not close error %s\n", cFsac_name);
        exit(1);
    }
    if (NULL == (ptFile_sac = fopen(cFsac_name, "wb"))) {
        fprintf(stderr, "SAC file open error %s\n", cFsac_name);
        exit(1);
    }
 
    if (giKbinary == 1) {  /** バイナリーファイル作成の時 **/
        if (ptFile_bin != NULL) {
            fprintf(stderr, "BINARY file not close error %s\n", cFbin_name);
            exit(1);
        }
        if (NULL == (ptFile_bin = fopen(cFbin_name, "wb"))) {
            fprintf(stderr, "BINARY file open error %s\n", cFbin_name);
            exit(1);
        }
    }
    if (giKascii == 1) {  /** アスキーファイル作成の時 **/
        if (ptFile_asc != NULL) {
            fprintf(stderr, "ASCII file not close error %s\n", cFasc_name);
            exit(1);
        }
        if (NULL == (ptFile_asc = fopen(cFasc_name, "w"))) {
            fprintf(stderr, "ASCII file open error %s\n", cFasc_name);
            exit(1);
        }
    }
    newhdr();
    sac_header.npts = npts;
    sac_header.b = beg;
    sac_header.leven = true;
    sac_header.delta = del;
    sac_header.ievtyp = IQUAKE;
    sac_header.nzyear = nzyear;
    sac_header.nzjday = nzjday;
    sac_header.nzhour = nzhour;
    sac_header.nzmin = nzmin;
    sac_header.nzsec = nzsec;
    sac_header.nzmsec = nzmsec;
    ii1 = GS_NUMBER(sac_header.kstnm);
    ii2 = strlen(kstnm);
    ii3 = GS_MIN(ii1-1, ii2);
    memset(sac_header.kstnm, (int)NULL, ii1);
    strncpy(sac_header.kstnm, kstnm, ii3);
    strncpy(sac_header.kevnm, "                ", 16);
    if (giKwin32 != 0) {
        if (gcOrganize1 == (unsigned char)0x01) {
            if (gcOrganize2 == (unsigned char)0x01) {
                strncpy(sac_header.kevnm, "Hi-net          ", 16);
            } else if (gcOrganize2 == (unsigned char)0x02) {
                strncpy(sac_header.kevnm, "APE             ", 16);
            } else if (gcOrganize2 == (unsigned char)0x03) {
                strncpy(sac_header.kevnm, "F-net           ", 16);
            } else if (gcOrganize2 == (unsigned char)0x05) {
                strncpy(sac_header.kevnm, "V-net           ", 16);
            }
        } else if (gcOrganize1 == (unsigned char)0x02) {
            strncpy(sac_header.kevnm, "Univ.           ", 16);
        } else if (gcOrganize1 == (unsigned char)0x03) {
            strncpy(sac_header.kevnm, "JMA             ", 16);
        }
    } else {
        strncpy(sac_header.kevnm, "Hi-net          ", 16);
    }
    ii1 = GS_NUMBER(sac_header.kcmpnm);
    ii2 = strlen(kcmp);
    ii3 = GS_MIN(ii1-1, ii2);
    memset(sac_header.kcmpnm, (int)NULL, ii1);
    strncpy(sac_header.kcmpnm, kcmp, ii3);
#ifdef NETWK
    strcpy(sac_header.knetwk, NETWK);
#endif
    sac_header.cmpaz = cmpaz;
    sac_header.cmpinc = cmpinc;
    sac_header.stla = stla;
    sac_header.stlo = stlo;
    sac_header.stel = stel;
    iKer = pickfile_read(uiSysch, winfile,
        &nzyear,
        &nzjday,
        &nzhour,
        &nzmin,
        &nzsec,
        &o,         /** 発振時刻が波形ファイルの先頭時刻から何秒後か **/
        &stla,
        &stlo,
        &stel,
        &evla,      /** latitude **/
        &evlo,      /** longitude **/
        &evdp,      /** depth **/
        &dist,
        &az,        /** 震央距離 **/
        &a,         /** 波形ファイルの先頭時刻からのＰ−time **/
        &t9,        /** 波形ファイルの先頭時刻からのＳ−time **/
        cUD,        /** 初動極性 **/
        cUNE        /** チャンネルテーブルの成分コード **/
        );
    if (strcmp(sunit, "m/s") == 0) {
        sac_header.idep = 7;  /** nm/s **/
    } else if (strcmp(sunit, "m/s/s") == 0) {
        sac_header.idep = 8;  /** nm/s/s **/
    } else if (strcmp(sunit, "rad") == 0) {
        sac_header.idep = 10; /** micro rad **/
    }
    if (iKer == 0) {
        sac_header.nzsec = 0;           /** TEST TEST **/
        sac_header.o = o;               /** 発振時刻が波形ファイルの先頭時刻から何秒後か **/
        sac_header.evla = evla;         /** latitude **/
        sac_header.evlo = evlo;         /** longitude **/
        sac_header.evdp = evdp;         /** depth **/
        sac_header.dist = dist;         /** default(-12345.0) **/
        sac_header.az = az;             /** 震央距離 **/
        sac_header.a = a;               /** 波形ファイルの先頭時刻からのＰ−time **/
        sac_header.t9 = t9;             /** 波形ファイルの先頭時刻からのＳ−time **/
        strcpy(sac_header.kt9, "");
        if (sac_header.t9 != -12345.0) {
            strcpy(sac_header.kt9, "S");
        }
        strcpy(sac_header.ka, "");
        if (strcmp(cUD, ".") == 0) {
            strcpy(sac_header.ka, "P");
        }
        if (strcmp(cUD, "U") == 0 || strcmp(cUD, "u") == 0) {
            strcpy(sac_header.ka, "PU");
        }
        if (strcmp(cUD, "D") == 0 || strcmp(cUD, "d") == 0) {
            strcpy(sac_header.ka, "PD");
        }
        pc1 = strstr(cUNE, "U");
        if (pc1 == NULL) {
            pc1 = strstr(cUNE, "u");
            if (pc1 == NULL) {
                pc1 = strstr(cUNE, "Z");
                if (pc1 == NULL) {
                    pc1 = strstr(cUNE, "z");
                }
            }
        }
        pc2 = strstr(cUNE, "N");
        if (pc2 == NULL) {
            pc2 = strstr(cUNE, "n");
            if (pc2 == NULL) {
                pc2 = strstr(cUNE, "X");
                if (pc2 == NULL) {
                    pc2 = strstr(cUNE, "x");
                }
            }   
        }
        pc3 = strstr(cUNE, "E");
        if (pc3 == NULL) {
            pc3 = strstr(cUNE, "e");
            if (pc3 == NULL) {
                pc3 = strstr(cUNE, "Y");
                if (pc3 == NULL) {
                    pc3 = strstr(cUNE, "y");
                }
            }   
        }
        sac_header.cmpaz = 0.0;
        sac_header.cmpinc = 0.0;
        if (pc1 != NULL) {  /** 成分コードにUまたはZがあるとき **/
            sac_header.cmpaz = 0.0;
            sac_header.cmpinc = 0.0;
        } else if (pc2 != NULL) {  /** 成分コードにNまたはXがあるとき **/
            sac_header.cmpaz = 0.0;
            sac_header.cmpinc = 90.0;
        } else if (pc3 != NULL) {  /** 成分コードにEまたはYがあるとき **/
            sac_header.cmpaz = 90.0;
            sac_header.cmpinc = 90.0;
        }
    } else {
        sac_header.nzsec = 0;           /** for original win2sac bug **/
    }
    if (giKendian == 0) {
        swap_header(&sac_header);
    }
    fwrite(&sac_header, sizeof(sac_header), 1, ptFile_sac);  /** サックファイルにヘッダーを書く **/
    for (ia=0; ia<npts; ia++) {
        if (giKascii == 1) {  /** アスキーファイルに書く(エンディアン変換する前に) **/
            iKer = fprintf(ptFile_asc, "%g\n", yfunc[ia]*gfRatio);
        }
        if (giKbinary == 1) {
            uni.f = yfunc[ia]*gfRatio;
            if (giKendian == 0) {  /** ビッグエンディアンにする **/
                swap4b((unsigned int *)&uni.ul);
            }
            fwrite(&uni.f, 4, (size_t) 1, ptFile_bin);
        }
        if (giKendian == 0) {  /** ビッグエンディアンにする **/
            swap4b((unsigned int *)(yfunc+ia));
        }
    }
    fwrite(yfunc, 4, (size_t) npts, ptFile_sac);
    fclose(ptFile_sac);
    ptFile_sac = NULL;
    if (giKbinary == 1) {
        fclose(ptFile_bin);
        ptFile_bin = NULL;
    }
    if (giKascii == 1) {
        fclose(ptFile_asc);
        ptFile_asc = NULL;
    }
    iRet = 0;
ret:;
    return(iRet);
}

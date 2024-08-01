#include <s4win2sac.h>
#include        <string.h>
#include        <stdlib.h>
#define GS_NUMBER(arr)       ((int) (sizeof(arr) / sizeof(arr[0])))     /** 配列の大きさ **/
/* @(#)win2sac_32 Ver 1.02 2002/09/17 */
/* @(#)win2sac_32 Ver 1.01 2002/07/22 */
/* @(#)win2sac.c 2.13 98/05/02 19:43:37 */
/* Format conversion from WIN format to SAC format */
/* program dewin  1994.4.11-4.20  urabe */
/* 10KHz sampling format available */
#include <stdio.h>
#include <signal.h>
#include <math.h>
#include <string.h>
#define  TRUE 1
#define  FALSE 0
#define DEBUG 0
#define DEBUG1 0
/* #define MAX 1000000 */
#define MAX 2000000
#define NETWK "HYOGO"
#define INUCL 37
#define IPREN 38
#define IPOSTN 39
#define IQUAKE 40
#define IPREQ 41
#define IPOSTQ 42
#define ICHEM 43
#define IOTHER 44
#define ITIME 1
#define IRLIM 2
#define IAMPH 3
#define IXY 4
#define NVHDR 6
int
get_channel(
    char * pcParameter,                 /** ( I ) パラメーターの内容 **/
    int  * piNchannel,                  /** ( O ) 得られたチャンネルの数 **/
    unsigned int **ppuiChid             /** ( O ) 得られたチャンネル番号 **/
);
char    daytab[2][13] = {
    {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31},
    {0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
};
_sac_header sac_header;
_sac_hdr2 sac_hdr2;
float   gfRatio;
float   *yfunc;
int     giNpmax;
int     buf[2000];
char    winfile[BUFSIZ], winfiled[BUFSIZ], sacfile[BUFSIZ];
char    gcBinext[50];
char    gcAscext[50];
char    cFileprm[1024];
char    cbuf[BUFSIZ];
unsigned int     sysch;
char    cDirname[1024];
int     giKwin32;
int     giKendian;
int     giKbinary;
int     giKascii;
unsigned char    gcOrganize1;
unsigned char    gcOrganize2;
int     giKwidechan;
int 
main(int argc, char *argv[])
{
    int     iKer;
    int     iNchannel;
    unsigned int *puiChid;
    int     iRet = 0;
    int     ia;
    int     sr = 0;
    int     sr_before = 0;
    fpos_t  iHeadpos;
    int     iCount;
    int     iForm;
    int     i, j, k, sec, mainsize, sr_save;
    int     time1[6], time2[6], time3[6];
    static unsigned char *mainbuf = NULL;
    static FILE   *f_main = NULL;
    int     tptr;
    char   *token[20];
    int     iKprm;
    int     npts;
/*     static char ver[] = "@(#)win2sac.c 2.13 98/05/02 19:43:37"; */
/*     static char ver[] = "@(#)win2sac_32(NIED) Ver 1.01 2002/07/22"; */
/*     static char ver[] = "@(#)win2sac_32(NIED) Ver 1.02 2002/09/17"; */
/*     static char ver[] = "@(#)win2sac_32(NIED) Ver 2.00 2002/12/05"; */
/*     static char ver[] = "@(#)win2sac_32(NIED) Ver 2.10 2002/06/03"; */
/*    static char ver[] = "@(#)win2sac_32(NIED) Ver 2.20 2002/06/30"; */
/*     static char ver[] = "@(#)win2sac_32(NIED) Ver 2.22 2006/01/11"; */
/*     static char ver[] = "@(#)win2sac_32(NIED) Ver 2.50 2007/12/20"; */
    static char ver[] = "@(#)win2sac_32(NIED) Ver 2.50 2007/12/20";
    fprintf(stderr, "%s\n", ver);
    iKprm = 0;
    giNpmax = MAX;
    giKendian = 0;
    gfRatio = 1.0;
    strcpy(cFileprm, "");
    strcpy(gcBinext, "");
    strcpy(gcAscext, "");
    giKwidechan = 0;
    if (argc > 1) {
        /** parameter file check **/
        for (ia = 0; ia < argc; ia++) {
            if (strlen(argv[ia]) > 2 &&
                (strncmp(argv[ia], "-p", 2) == 0 || strncmp(argv[ia], "-P", 2) == 0)) {
                strcpy(cFileprm, argv[ia] + 2);
                iKprm++;
                break;
            }
        }
        /** endian check **/
        for (ia = 0; ia < argc; ia++) {
            if ( (strcmp(argv[ia], "-e") == 0 || strcmp(argv[ia], "-E") == 0)) {
                giKendian = 1;
                iKprm++;
                break;
            }
        }
        /** binary file extender **/
        for (ia = 0; ia < argc; ia++) {
            if ( (strncmp(argv[ia], "-b", 2) == 0 || strncmp(argv[ia], "-B", 2) == 0)) {
                giKbinary = 1;
                if (strlen(argv[ia]) > 2 && strlen(argv[ia]) <= GS_NUMBER(gcBinext)-1+2) {
                    strcpy(gcBinext, argv[ia] + 2);
                } else {
                    strcpy(gcBinext, "bin");
                }
                iKprm++;
                break;
            }
        }
        /** ascii file extender **/
        for (ia = 0; ia < argc; ia++) {
            if ( (strncmp(argv[ia], "-a", 2) == 0 || strncmp(argv[ia], "-A", 2) == 0)) {
                giKascii = 1;
                if (strlen(argv[ia]) > 2 && strlen(argv[ia]) <= GS_NUMBER(gcAscext)-1+2) {
                    strcpy(gcAscext, argv[ia] + 2);
                } else {
                    strcpy(gcAscext, "asc");
                }
                iKprm++;
                break;
            }
        }
        /** maximum of point **/
        for (ia = 0; ia < argc; ia++) {
            if ( (strncmp(argv[ia], "-m", 2) == 0 || strncmp(argv[ia], "-M", 2) == 0)) {
                giNpmax = 0;
                if (strlen(argv[ia]) > 2) {
                    giNpmax = atoi(argv[ia] + 2);
                }
                iKprm++;
                break;
            }
        }
        /** ratio of bin-file and asc-file **/
        for (ia = 0; ia < argc; ia++) {
            if ( (strncmp(argv[ia], "-r", 2) == 0 || strncmp(argv[ia], "-R", 2) == 0)) {
                gfRatio = -999.0;
                if (strlen(argv[ia]) > 2) {
                    gfRatio = atof(argv[ia] + 2);
                }
                iKprm++;
                break;
            }
        }  
        /** wide chanel ? **/
        for (ia = 0; ia < argc; ia++) {
            if ( strncmp(argv[ia], "-Y", 2) == 0 ) {
                giKwidechan = 1;
                break;
            }
        }
    }
    if (cFileprm[0] == '\0') {
        strcpy(cFileprm, "./win.prm");
    }
    if ( argc-iKprm < 4) {
        fprintf(stderr, "usage: %s winfile ch_no sacfile [outdir] [-p(prmfile)]\n", argv[0]);
        fprintf(stderr, "          [-Y] [-e] [-b[BIN]] [-a[ASC]] [-r(RATIO)] [-m(PMAX)]\n");
        iRet = 1;
        goto ret;
    }
    if (giNpmax <= 0) {
        fprintf(stderr, "***** The number of maximum point is error.(%d)\n", giNpmax);
        exit(0);
    } else {
        yfunc = calloc(giNpmax, sizeof(float));
        if (yfunc == NULL) {
            fprintf(stderr, "***** ERROR ***** Memory allocation error.\n");
            exit(0); 
        }
    }
    if (gfRatio <= 0.0) {
        fprintf(stderr, "***** The ratio of bin-file and asc-file is error.(%f)\n", gfRatio);
        exit(0);
    }
    if (argc >= 5 && strncmp(argv[4], "-", 1) != 0) {
        strcpy(cDirname, argv[4]);
        if (cDirname[(int) strlen(cDirname) - 1] != '/') {
            strcat(cDirname, "/");
        }
    } else {
        strcpy(cDirname, "./");
    }
/* get winfile name including directory name */
    strcpy(winfiled, argv[1]);
/*     printf("----------- argv[1]=%s\n", argv[1]); */
/*     iHeadpos = (fpos_t)0; */
    if (f_main != NULL) {
        perror(argv[0]);
        iRet = 1;
        goto ret;
    }
    f_main = fopen(argv[1], "rb");
    if (f_main == NULL) {
        perror(argv[0]);
        iRet = 1;
        goto ret;
    }
    fgetpos(f_main, &iHeadpos);
    iCount = fread(&iForm, 1, 4, f_main);
    if (iCount != 4) {
        perror(argv[0]);
        iRet = 1;
        goto ret;
    }
    if (iForm == 0) {
        giKwin32 = 1;
    } else {
        giKwin32 = 0;
        fsetpos(f_main, &iHeadpos);
    }
    fclose(f_main);
    f_main = NULL;
/* get only file name part */
    strcpy(cbuf, winfiled);
    if ((char *) NULL != (token[0] = strtok(cbuf, "/"))) {
        tptr = 1;
        while ((char *) NULL != (token[tptr] = strtok(NULL, "/")))
            tptr++;
        strcpy(winfile, token[tptr - 1]);
    } else {
        strcpy(winfile, winfiled);
    }
    fprintf(stderr, "winfile = %s\n", winfile);
/*     sysch = strtoul(argv[2], 0, 16); */
    iKer = get_channel(
               argv[2],                 /** ( I ) パラメーターの内容 **/
               &iNchannel,              /** ( O ) 得られたチャンネルの数 **/
               &puiChid                 /** ( O ) 得られたチャンネル番号 **/
           );
    if (iNchannel == 0 || iKer) {
        fprintf(stderr,"The channel number get error.\n");
        exit(0);
    }
    mainbuf = NULL;
    for (ia=0; ia<iNchannel; ia++) {
        fprintf(stderr,"\n");
        fprintf(stdout,"\n");
        npts = 0;
        if (mainbuf != NULL) free(mainbuf);
        mainbuf = NULL;
        if (f_main != NULL) {
            perror(argv[0]);
            iRet = 1;
            goto ret;
        }
        f_main = fopen(argv[1], "rb");
        if (f_main == NULL) {
            perror(argv[0]);
            iRet = 1;
            goto ret;
        }
        fgetpos(f_main, &iHeadpos);
        iCount = fread(&iForm, 1, 4, f_main);
        if (iCount != 4) {
            perror(argv[0]);
            iRet = 1;
            goto ret;
        }
        if (iForm == 0) {
            giKwin32 = 1;
        } else {
            giKwin32 = 0; 
            fsetpos(f_main, &iHeadpos);
        }          
        sysch = puiChid[ia];
/*         printf("---------- sysch=%d\n", sysch); */
        strcpy(sacfile, argv[3]);
#if DEBUG
        fprintf(stderr, "sysch = %08x\n", sysch);
#endif
        sec = sr_save = i = 0;
        while ((mainsize = read_data(&mainbuf, f_main))) {
/*             printf("mainsize=%d\n", mainsize); */
            if ((sr = read_one_sec(mainbuf, sysch, (int *) buf)) == 0)
                continue;
/*         printf("sr=%d\n", sr); */
            sr_before = sr;
            if (giKwin32 == 0) {
                bcd_dec(time3, (char *) (mainbuf + 4));
            } else {
                bcd_dec(time3, (char *) (mainbuf + 5));
            }
#if 1
            fprintf(stdout, "time = %02d%02d%02d.%02d%02d%02d\n",
                time3[0], time3[1], time3[2], time3[3], time3[4], time3[5]);
#endif
            if (sr_save == 0) {
                if (giKwidechan == 0) {
                    fprintf(stderr, "\n%04X  %d Hz  ", sysch, sr);
                } else {
                    fprintf(stderr, "\n%08X  %d Hz  ", sysch, sr);
                }
                if (giKwin32 == 0) {
                    bcd_dec(time1, (char *) (mainbuf + 4));
                } else {
                    bcd_dec(time1, (char *) (mainbuf + 5));
                }
                fprintf(stderr, "%02d%02d%02d.%02d%02d%02d -> ",
                    time1[0], time1[1], time1[2], time1[3], time1[4], time1[5]);
            }
            if (sr_save) {
                time2[5]++;
                adj_time(time2);
                if (time_cmp(time2, time3) > 0) {
                    fprintf(stderr,"***** EOOR ***** The time is not sort.(%06d%06d--- %06d%06d)\n",
                           time2[0]*10000+time2[1]*100+time2[2],time2[3]*10000+time2[4]*100+time2[5],
                           time3[0]*10000+time3[1]*100+time3[2],time3[3]*10000+time3[4]*100+time3[5]);
                    exit (0);
                }
                while (time_cmp(time2, time3) < 0) {
                    k = 0;
                    for (j = 0; j < sr_save; j++) {
                        if (npts >= giNpmax) {
                            fprintf(stderr,"***** ERROR ***** The number of points is maximum over.(%d)\n",
                                 giNpmax);
                            exit (0);
                        }
                        yfunc[npts] = (float) k;
                        npts++;
                    }
    
                    i++;
                    time2[5]++;
                    adj_time(time2);
                }
            }
            for (j = 0; j < sr; j++) {
                if (npts >= giNpmax) {
                    fprintf(stderr,"***** ERROR ***** The number of points is maximum over.(%d)\n", giNpmax);
                    exit (0);
                }
                yfunc[npts] = (float) buf[j];
                npts++;
            }
    
            i++;
            sr_save = sr;
            if (giKwin32 == 0) {
                bcd_dec(time2, (char *) (mainbuf + 4));
            } else {
                bcd_dec(time2, (char *) (mainbuf + 5));
            }
            sec++;
        }
    
    
        if (sec != 0) {
            fprintf(stderr, "%02d%02d%02d.%02d%02d%02d (%d[%d] s)\n",
                time3[0], time3[1], time3[2], time3[3], time3[4], time3[5], i, sec);
            if (sr == 0) {
                sr = sr_before;
            }
            if (sr == 0) {
                fprintf(stderr,"***** Illegal win data.\n");
                exit(0);
            }
            win2sac0(npts, sr, sysch, time1);
            iRet = 0;
        } else {
            fprintf(stderr, "Data for channel %x not existed\n", sysch);
            iRet = 1;
        }
        fclose(f_main);
        f_main = NULL;
        if (iRet != 0) goto ret;
    }
ret:;
    exit(iRet);
}

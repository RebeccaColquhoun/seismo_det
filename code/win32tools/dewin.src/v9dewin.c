#ifdef MINGW
#include <fcntl.h>
#include <io.h>
#endif
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <v9dewin_man.h>
/* program dewin  1994.4.11-4.20  urabe */
/*                1996.2.23 added -n option */
/*                1996.9.12 added -8 option */
/*                1998.5.16 LITTLE ENDIAN and High Sampling Rate (uehira) */
/*                1998.5.18 add -f [filter file] option (uehira) */
/*                1998.6.26 yo2000 urabe */
int     giKbegin;
int     giKwin32;
int     giKwrite;
int     giKwidechan;
void    ctrlc();
extern int getopt(int argc, char * const argv[], const char *optstring);
int 
main(int argc, char *argv[])
{
    int     iAbsent_sr = 0;
    int     ia;
    int     ib;
    int     iSec;
    int     iSecp;
    int     iKer;
    int     iNchannel;
    unsigned int *puiChid;
    int     iKextend;
    char    cExtend[100];
    char    cWfile[100];
    FILE   *ptFile_ext = NULL;
    int * piTime2;
    int * piTime3;
    int     i, j, k, iNormal, mainsize, sr_save, c, form, iKfill, time1[8];
    unsigned int uiSysch;
    int iPrint;
    int sr = 0;
    int zero = 0;
    static int time2[8] = {0,0,0,0,0,0,0,0};
    static int time3[8] = {0,0,0,0,0,0,0,0};
    static unsigned char *mainbuf;
    FILE   *f_main = NULL;
    FILE   *f_filter = NULL;
    unsigned char cc;
    extern int optind;
    extern char *optarg;
    char    txtbuf[LINELEN];
    int     filter_flag;
    struct Filter flt;
    double  uv[MAX_FILT * 4];
#ifdef MINGW
    int result;
#endif
/*    static char ver[] = "@(#)dewin_32(NIED) Ver 2.00 2003/01/27"; */
/*     static char ver[] = "@(#)dewin_32(NIED) Ver 2.10 2003/01/27"; */
/*     static char ver[] = "@(#)dewin_32(NIED) Ver 2.50 2007/12/20"; */
#ifdef MINGW
   /* "stdin" をバイナリ モードに設定します。 */
    result=_setmode(_fileno(stdin),O_BINARY);
    if( result == -1 ) {
        fprintf(stderr, "***** ERROR ***** The mode does not set.(%s %d)\n",
                __FILE__, __LINE__);
       exit(0);
    }
#endif
/*     fprintf(stderr, "%s\n", ver); */
    giKwrite = 0;
    giKbegin = 1;                       /* It has never been read yet. */
    giKwin32 = 0;                       /* The matter that it is not
                                         * WIN32 is set up. */
    signal(SIGINT, ctrlc);
    signal(SIGTERM, ctrlc);
    form = 0;
    iKfill = 1;
    filter_flag = 0;
    for (i = 0; i < MAX_FILT * 4; ++i) {
        uv[i] = 0.0;
    }
    iKextend = 0;
    cExtend[0] = '\0';
    giKminutes = 0;
    giNsample = 0;
    giKwidechan = 0;
    while ((c = getopt(argc, argv, "Ys:mchnaf:e:")) != EOF) {
        switch (c) {
        case 'Y':
            giKwidechan = 1;             /* wide chanel? */
            break;
        case 's':                       /* sampling number */
            if (NULL == optarg) {
                fprintf(stderr, "The parameter of sampling number is error.\n");
                exit(1);
            }
            giNsample = atoi(optarg);
            if (giNsample <= 0 || giNsample > 2000) {
                fprintf(stderr, "The sampling number is equal zero or over 2000.\n");
                exit(1);
            }
            break;
        case 'm':
            giKminutes = 1;             /* minutes file */
            break;
        case 'a':
            form = 8;                   /* 8bit format output */
            break;
        case 'c':
            form = 1;                   /* numerical character output */
            break;
        case 'n':
            iKfill = 0;                 /* don't fill absent seconds */
            break;
        case 'e':                       /* output file extend */
            if (NULL == optarg || strlen(optarg) > 100-1) {
                fprintf(stderr, "The parameter of extend is error.\n");
                exit(1);
            }
            iKextend = 1;
            strcpy(cExtend, optarg);
            break;
        case 'f':                       /* filter output */
            if (optarg == NULL) {
                fprintf(stderr, "The filter file name is nothing.\n");
                exit(1);
            }
            if (f_filter != NULL) {
                fclose(f_filter);
            }
#ifdef MINGW
            if (optarg == NULL || NULL == (f_filter = fopen(optarg, "rt"))) {
                fprintf(stderr, "Cannot open filter parameter file: %s\n", optarg);
                exit(1);
            }
#else
            if (optarg == NULL || NULL == (f_filter = fopen(optarg, "r"))) {
                fprintf(stderr, "Cannot open filter parameter file: %s\n", optarg);
                exit(1);
            }
#endif
            while (!feof(f_filter)) {
                if (fgets(txtbuf, LINELEN, f_filter) == NULL) {
                    fputs("No filter parameter.\n", stderr);
                    exit(1);
                }
                if (*txtbuf == '#')
                    continue;
                sscanf(txtbuf, "%3s", flt.kind);
                if (strcmp(flt.kind, "LPF") == 0 || strcmp(flt.kind, "lpf") == 0) {
                    strcpy(flt.kind, "LPF");
                } else if (strcmp(flt.kind, "HPF") == 0 || strcmp(flt.kind, "hpf") == 0) {
                    strcpy(flt.kind, "HPF");
                } else if (strcmp(flt.kind, "BPF") == 0 || strcmp(flt.kind, "bpf") == 0) {
                    strcpy(flt.kind, "BPF");
                } else {
                    fprintf(stderr, "bad filter name '%s'\n", flt.kind);
                    exit(1);
                }
                for (j = 0; j < strlen(txtbuf) - 3; j++) {
                    if (strncmp(txtbuf + j, "fl=", 3) == 0)
                        sscanf(txtbuf + j + 3, "%lf", &flt.fl);
                    else if (strncmp(txtbuf + j, "fh=", 3) == 0)
                        sscanf(txtbuf + j + 3, "%lf", &flt.fh);
                    else if (strncmp(txtbuf + j, "fp=", 3) == 0)
                        sscanf(txtbuf + j + 3, "%lf", &flt.fp);
                    else if (strncmp(txtbuf + j, "fs=", 3) == 0)
                        sscanf(txtbuf + j + 3, "%lf", &flt.fs);
                    else if (strncmp(txtbuf + j, "ap=", 3) == 0)
                        sscanf(txtbuf + j + 3, "%lf", &flt.ap);
                    else if (strncmp(txtbuf + j, "as=", 3) == 0)
                        sscanf(txtbuf + j + 3, "%lf", &flt.as);
                }
                if (!(strcmp(flt.kind, "LPF") == 0 && flt.fp < flt.fs) &&
                    !(strcmp(flt.kind, "HPF") == 0 && flt.fs < flt.fp) &&
                    !(strcmp(flt.kind, "BPF") == 0 && flt.fl < flt.fh && flt.fh < flt.fs)) {
                    fprintf(stderr, "%s %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f",
                        flt.kind, flt.fl, flt.fh, flt.fp, flt.fs, flt.ap, flt.as);
                    fprintf(stderr, " : illegal filter\n");
                    exit(1);
                }
                break;
            }
            filter_flag = 1;
            break;
        case 'h':
        default:
            print_usage();
            exit(1);
        }
    }
#ifdef MINGW
    if (form != 1) {
       /* "stdout" をバイナリ モードに設定します。 */
        result = _setmode( _fileno( stdout ), _O_BINARY );
        if( result == -1 ) {
            fprintf(stderr, "***** ERROR ***** The mode does not set.(%s %d)\n",
                    __FILE__, __LINE__);
           exit(0);
        }
    }
#endif
    if (filter_flag) {
        fputs("Type  Low  High  Pass  Stop    AP    AS\n", stderr);
        fprintf(stderr, "%s %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f\n",
            flt.kind, flt.fl, flt.fh, flt.fp, flt.fs, flt.ap, flt.as);
    }
    optind--;
    if (argc < optind + 2) {
        print_usage();
        exit(1);
    }
    if (iKfill == 0 && (giKminutes != 0 || giNsample != 0)) {
        fprintf(stderr,"If absent data does not output, -m & -s parameters are ignored.\n");
        giKminutes = 0;
        giNsample = 0;
    }
    iKer = get_channel(
               argv[optind + 1],        /** ( I ) パラメーターの内容 **/
               &iNchannel,              /** ( O ) 得られたチャンネルの数 **/
               &puiChid                 /** ( O ) 得られたチャンネル番号 **/
           );
    if (iNchannel == 0 || iKer) {
        fprintf(stderr,"The channel number get error.\n");
        exit(1); 
    }   
    if (argc < 3 + optind && iNchannel > 1) {
        fprintf(stderr, "When multiple channels, specify file name!.\n");
        exit (1);
    }
    if (iKextend == 0 && iNchannel > 1) {
        fprintf(stderr, "When multiple channels, specify extend name!.\n");  
        exit (1);
    }
    for (ia=0; ia<iNchannel; ia++) {
        giKwrite = 0;
        giKbegin = 1;                       /* It has never been read yet. */
        giKwin32 = 0;                       /* The matter that it is not
                                             * WIN32 is set up. */
        for (i = 0; i < MAX_FILT * 4; ++i) {
            uv[i] = 0.0;  
        }
        uiSysch = puiChid[ia];
        if (iKextend == 1) {
            if (giKwidechan == 0) {
                sprintf(cWfile, "%04x", uiSysch);
            } else {
                sprintf(cWfile, "%08x", uiSysch);
            }
            strcat(cWfile, ".");
            if (strlen(cWfile)+strlen(cExtend) > 100-1) {
                fprintf(stderr, "Output file name is too long!.(%s%s)\n",cWfile,cExtend);
                exit(1);
            }
            strcat(cWfile, cExtend);
            if (ptFile_ext != NULL && ptFile_ext != stdout) {
                fclose(ptFile_ext);
            }
#ifdef MINGW
            if (form == 1) {
                ptFile_ext = fopen(cWfile, "wt");
            } else {
                ptFile_ext = fopen(cWfile, "wb");
            }
#else
            ptFile_ext = fopen(cWfile, "w");
#endif
            if (ptFile_ext == NULL) {
                fprintf(stderr, "Output file open error!.(%s)\n",cWfile);
                exit(1);
            }
        } else {
            ptFile_ext = stdout;
        }
        if (argc < 3 + optind) {
            f_main = stdin;
#ifdef MINGW
        } else if ((f_main = fopen(argv[2 + optind], "rb")) == NULL) {
            perror("dewin");
            exit(1);
#else
        } else if ((f_main = fopen(argv[2 + optind], "r")) == NULL) {
            perror("dewin");
            exit(1);
#endif
        }
        iNormal = sr_save = iPrint = 0;
        while ((mainsize = read_data(&mainbuf, f_main)) != 0) {
            if ((sr = read_one_sec(mainbuf, uiSysch, (int *)buf)) == 0) {
                continue;
            }
            if (giKwin32 == 0) {
                bcd_dec(time3, (char *)(mainbuf + 4));
            } else {
                bcd_dec8(time3, (char *)(mainbuf + 4));
            }
            iAbsent_sr = sr;  /** when absent output sampling number **/
            if (sr_save == 0) {  /** first time **/
                iSec = time3[6];
                if (giKwin32 == 0) iSec = time3[5];
                iSecp = iSec;
                if (giKminutes == 1 && iSec > 0 && iKfill == 1) {  /** absent seconds **/
                    iSecp = 0;
                    for (ib=0; ib<iSec; ib++) {
                        k = 0;
                        cc = 128;
                        if (form == 1) {
                            for (j = 0; j < iAbsent_sr; j++) {
                                fprintf(ptFile_ext, "0\n");
                            }
                        } else if (form == 8) {
                            for (j = 0; j < iAbsent_sr; j++) {
                                fwrite(&cc, 1, 1, ptFile_ext);
                            }
                        } else {
                            for (j = 0; j < iAbsent_sr; j++) {
                                fwrite(&k, 4, 1, ptFile_ext);
                            }
                        }
                        iPrint++;
                    }
                } else {
                    iSecp = iSec;
                }
                if (giKwidechan == 0) {
                    fprintf(stderr, "%04X  %d Hz  ", uiSysch, sr);
                } else {
                    fprintf(stderr, "%08X  %d Hz  ", uiSysch, sr);
                }
                if (giKwin32 == 0) {
                    bcd_dec(time1, (char *)(mainbuf + 4));
                    fprintf(stderr, "%02d%02d%02d.%02d%02d%02d -> ",
                        time1[0], time1[1], time1[2], time1[3], time1[4], iSecp);
                } else {
                    bcd_dec8(time1, (char *)(mainbuf + 4));
                    fprintf(stderr, "%02d%02d%02d%02d.%02d%02d%02d(%02d) -> ",
                        time1[0], time1[1], time1[2], time1[3], time1[4],
                        time1[5], iSecp,    time1[7]);
                }
                if (form == 8) {
                    fwrite(au_header, sizeof(au_header), 1, ptFile_ext);
                }
            } else {
                /** seconds plus **/
                if (giKwin32 == 0) {
                    time2[5]++;
                } else {
                    time2[6]++;
                }
                if (giKwin32 == 0) {
                    adj_time(time2);
                } else {
                    adj_time2(time2);
                }
    
    
                if (giKwin32 == 0) {
                    piTime2 = &time2[0];
                    piTime3 = &time3[0];
                } else {
                    piTime2 = &time2[1];
                    piTime3 = &time3[1];
                }
                while (1) {
                    iKer = time_cmp(piTime2, piTime3, 6);
                    if (iKer < 0) {     /* fill absent data */
                        if (iKfill == 1) {
                            k = 0;
                            cc = 128;
                            if (form == 1) {
                                for (j = 0; j < sr_save; j++) {
                                    fprintf(ptFile_ext, "0\n");
                                }
                            } else if (form == 8) {
                                for (j = 0; j < sr_save; j++) {
                                    fwrite(&cc, 1, 1, ptFile_ext);
                                }
                            } else {
                                for (j = 0; j < sr_save; j++) {
                                    fwrite(&k, 4, 1, ptFile_ext);
                                }
                            }
                            iPrint++;
                        }
                        if (giKwin32 == 0) {
                            time2[5]++;
                            adj_time(time2);
                        } else {
                            time2[6]++;
                            adj_time2(time2);
                        }
                    } else if (iKer > 0) {
                        fprintf(stderr, "\n     Time is error. ");
                        if (giKwin32 == 0) {
                            fprintf(stderr, "%02d%02d%02d.%02d%02d%02d > ",
                                time2[0], time2[1], time2[2], time2[3], time2[4], time2[5]);
                            fprintf(stderr, "%02d%02d%02d.%02d%02d%02d\n",
                                time3[0], time3[1], time3[2], time3[3], time3[4], time3[5]);
                        } else {
                            fprintf(stderr, "%02d%02d%02d%02d.%02d%02d%02d(%02d) > ",
                                time2[0], time2[1], time2[2], time2[3], time2[4],
                                time2[5], time2[6], time2[7]);
                            fprintf(stderr, "%02d%02d%02d%02d.%02d%02d%02d(%02d)\n",
                                time3[0], time3[1], time3[2], time3[3], time3[4],
                                time3[5], time3[6], time3[7]);
                        }                       
                        break;
                    } else {
                        break;
                    }
                }
            }
            if (filter_flag) {
                get_filter(sr, &flt);
                /* fprintf(stderr,"m_filt=%d\n",flt.m_filt); */
                for (j = 0; j < sr; ++j)
                    dbuf[j] = (double) buf[j];
                tandem(dbuf, dbuf, sr, flt.coef, flt.m_filt, 1, uv);
                for (j = 0; j < sr; ++j)
                    buf[j] = (int) (dbuf[j] * flt.gn_filt);
            }
            if (form == 1) {
                for (j = 0; j < sr; j++) {
                    fprintf(ptFile_ext, "%d\n", buf[j]);
                }
            } else if (form == 8) {
                if (sr_save == 0) {
                    zero = 0;
                    for (j = 0; j < sr; j++) {
                        zero += buf[j];
                    }
                    zero /= sr;
                }
                for (j = 0; j < sr; j++) {
                    buf[j] -= zero;
                    cc = cvt(buf[j] * 256);
                    /* fprintf(stderr,"%d %d\n",buf[j],cc); */
                    fwrite(&cc, 1, 1, ptFile_ext);
                }
            } else {
                fwrite(buf, 4, sr, ptFile_ext);
            }
            iPrint++;
            sr_save = sr;
            if (giKwin32 == 0) {
                bcd_dec(time2, (char *)(mainbuf + 4));
            } else {
                bcd_dec8(time2, (char *)(mainbuf + 4));
            }
            iNormal++;
        }
        iSec = time3[6];
        if (giKwin32 == 0) iSec = time3[5];
        if (iNormal == 0) iSec = -1;  /** all absent **/
        if (giKminutes == 1 && iSec < 59 && iKfill == 1) {  /** absent seconds **/
            if (iSec == -1) {
                if (giNsample <= 0) {
                    fprintf(stderr, "If all absent, we need sampling number with -s parameter.\n");
                    exit(1);
                }
                iAbsent_sr = giNsample;
            }
            iSecp = 59;
            for (ib=iSec+1; ib<60; ib++) {
                k = 0;
                cc = 128;
                if (form == 1) {
                    for (j = 0; j < iAbsent_sr; j++) {
                        fprintf(ptFile_ext, "0\n");
                    }
                } else if (form == 8) {
                    for (j = 0; j < iAbsent_sr; j++) {
                        fwrite(&cc, 1, 1, ptFile_ext);
                    }
                } else {
                    for (j = 0; j < iAbsent_sr; j++) {
                        fwrite(&k, 4, 1, ptFile_ext);
                    }
                }
                iPrint++;
            }
        } else {
            iSecp = iSec;
            if (iSecp == -1) iSecp = 59;
        }
        if (giKwin32 == 0) {
            fprintf(stderr, "%02d%02d%02d.%02d%02d%02d (%d[%d] s)\n",
                time3[0], time3[1], time3[2], time3[3], time3[4], iSecp, iPrint, iNormal);
        } else {
            fprintf(stderr, "%02d%02d%02d%02d.%02d%02d%02d(%02d) (%d[%d] s)\n",
                time3[0], time3[1], time3[2], time3[3], time3[4],
                time3[5], iSecp, time3[7],iPrint, iNormal);
        }
        if (f_main != NULL && f_main != stdin) {
            fclose(f_main);
            f_main = NULL;
        }
        if (iKextend == 1) { 
            if (ptFile_ext != NULL && ptFile_ext != stdout) {
                fclose(ptFile_ext);
                ptFile_ext = NULL;
            }
        }       
    }
    exit(0);
}

#ifdef MINGW
#include <fcntl.h>
#include <io.h>
#endif
#include <unistd.h>
#include <string.h>
#include <v7wck_man.h>
#define MAX_WIDECHAN 100
int giKwidechan;
int giNwidechan;
int * piCount[MAX_WIDECHAN];
unsigned short int uhWidech[MAX_WIDECHAN];
int giKbegin;
int giKwin32;
int giKtime;
int giKnoch;
int giKprint;
int giKrawprint;
char gcTime[100];
char gcNoch[100];
int giTime[6];
unsigned int guiNoch;
extern void usage(void);
extern int read_data(unsigned char **ppucPtr, FILE   *ptFp);
extern int getopt(int argc, char * const argv[], const char *optstring);
extern void testmprc_();
void ctrlc();
int main(argc, argv)
    int     argc;
    char   *argv[];
{
    int kkkkkk;
#ifdef MINGW
    int result;
#endif
    int     i, j, mode, c, nch, sec, size, iMainsize, sr, gs, ts, ss;
    unsigned short int     uhSysch0;
    unsigned short int     uhSysch;
    unsigned int     uiWork;
    int ia;
    int     iii;
    int     iKall;
    char   *pc;
    int     iFlen = 0;
    FILE   *ptFile;
    char    cBytes[5];
    char    *pcProgname;
    static unsigned char *pucMainbuf = NULL;
    unsigned char *pucPtr0;
    unsigned char *pucPtr;
    unsigned char *pucPtr_lim;
    extern int optind;
    extern char *optarg;
/*     static char ver[] = "@(#)wck_32(NIED) Ver 1.10 2003/06/03"; */
/*     static char ver[] = "@(#)wck_32(NIED) Ver 1.50 2007/12/20"; */
#define RAW 0x00
#define MON 0x01
#define RAW_HSR 0x02
#define COUNT 0x10
#define SR_MON 5
/*     testmprc_(); */
/* exit(0); */
    kkkkkk = 0;
/*     fprintf(stderr, "%s\n", ver); */
    signal(SIGINT, ctrlc);
    signal(SIGTERM, ctrlc);
/*    signal(SIGPIPE, ctrlc); */
    if ((pcProgname = strrchr(argv[0], '/'))) {
        pcProgname++;
    } else {
        pcProgname = argv[0];
    }
    mode = RAW;
    giKrawprint = 0;
    giKtime = 0;
    giKnoch = 0;
    gcTime[0] = '\0';
    gcNoch[0] = '\0';
    iKall = 0;
    giKwidechan = 0;
    while ((c = getopt(argc, argv, "Ymrhcu?at:T:n:N:sS")) != EOF) {
        switch (c) {
        case 'Y':                       /* wide chanel mode */
            giKwidechan = 1;
            break;
        case 'c':                       /* "Count" mode */
            mode = (0x0f & mode) | COUNT;
            for (i = 0; i < 65536; i++) {
                count[i] = 0;
            }
            break;
        case 'm':                       /* MON data */
            mode = (0xf0 & mode) | MON;
            break;
        case 'r':                       /* RAW data */
            mode = (0xf0 & mode) | RAW;
            break;
        case 'a':                       /* details all print */
            iKall = 1;
            break; 
        case 't':                       /* details time option  */
        case 'T':                       /* details time option  */
            giKtime = 1;
            if (optarg != NULL) {
                giKtime = 2;
                strcpy(gcTime, optarg);
                if (strlen(gcTime) != 12 && strlen(gcTime) != 14) {
                    printf("***** ERROR ***** The time option error\n");
                    exit (1);
                }
                if (strlen(gcTime) == 12) {
                    sscanf(gcTime,"%02d%02d%02d%02d%02d%02d", &giTime[0], &giTime[1], &giTime[2],
                                                              &giTime[3], &giTime[4], &giTime[5]);
                    if (giTime[0] > 50) {
                        giTime[0] += 1900;
                    } else {
                        giTime[0] += 2000;
                    }
                } else {
                    sscanf(gcTime,"%02d%02d%02d%02d%02d%02d%02d", &iii, &giTime[0], &giTime[1], &giTime[2],
                                                              &giTime[3], &giTime[4], &giTime[5]);
                    giTime[0] += iii * 100;
                }
                printf("The time option = %04d%02d%02d%02d%02d%02d\n", giTime[0], giTime[1], giTime[2],
                                                                       giTime[3], giTime[4], giTime[5]);
            }
            break;
        case 'n':                       /* details noch option */
        case 'N':                       /* details noch option */
            giKnoch = 1;
            if (optarg != NULL) {
                giKnoch = 2;
                uiWork = strtoul(optarg, &pc, 16);
                if (pc[0] != '\0') {
                    printf("***** ERROR ***** The noch option error.\n");
                    exit(1);
                }
                guiNoch = (unsigned int)uiWork;
            
                printf("The noch option = %08x\n", guiNoch);
            }
            break;
        case 's':                       /* raw data print option */
        case 'S':                       /* raw data print option */
            giKrawprint = 1;
            break;
        case 'h':                       /* High sampling rate format
                                         * RAW data */
            mode = (0xf0 & mode) | RAW_HSR;
            break;
        case 'u':                       /* show usage */
        case '?':                       /* show usage */
        default:
            usage();
            exit(1);
        }
    }
    giKprint = 0;
    if (giKtime == 0 && giKnoch == 0) giKprint = 0;  /* no print */
    if (giKtime == 1 && giKnoch == 0) giKprint = 1;  /* print */
    if (giKtime == 2 && giKnoch == 0) giKprint = 2;  /* time print */
    if (giKtime == 0 && giKnoch == 1) giKprint = 1;  /* print */
    if (giKtime == 1 && giKnoch == 1) giKprint = 1;  /* print */
    if (giKtime == 2 && giKnoch == 1) giKprint = 2;  /* time print */
    if (giKtime == 0 && giKnoch == 2) giKprint = 3;  /* noch print */
    if (giKtime == 1 && giKnoch == 2) giKprint = 3;  /* noch print */
    if (giKtime == 2 && giKnoch == 2) giKprint = 4;  /** time & noch print */
    if (iKall == 1) giKprint = 1;  /* print */
/*     printf(" optind = %d\n", optind); */
    if (argc < optind + 1 || strcmp("-", argv[optind]) == 0) {
        ptFile = stdin;
#ifdef MINGW
   /* "stdin" ????? ?????????? */
    result=_setmode(_fileno(stdin), O_BINARY);
    if( result == -1 ) {
        fprintf(stderr, "***** ERROR ***** The mode does not set.(%s %d)\n",
                __FILE__, __LINE__);
       exit(0);
    }
#endif
    } else if ((ptFile = fopen(argv[optind], "rb")) == NULL) {
        usage();
        exit(1);
    }
    if (argc > optind + 1) {
        ss = atoi(argv[optind + 1]);
    } else {
        ss = 0;
    }
    giKbegin = 1;   /* It has never been read yet. */
    giKwin32 = 0;   /* The matter that it is not WIN32 is set up. */
    sec = ts = 0;
    while ((iMainsize = read_data(&pucMainbuf, ptFile))) {
        if (giKwin32 == 0) {
            pucPtr_lim = pucMainbuf + iMainsize;
        } else {
            pucPtr_lim = pucMainbuf + iMainsize + 4;
        }
        if (giKwin32 == 0) {
            pucPtr0 = pucMainbuf + 10;
            pucPtr = pucMainbuf + 10;
        } else {
            pucPtr0 = pucMainbuf + 20;
            pucPtr = pucMainbuf + 22;
        }
        nch = 0;
        do {
            uhSysch0 = pucPtr0[1] + (((int) pucPtr0[0]) << 8);
            uhSysch = pucPtr[1] + (((int) pucPtr[0]) << 8);
            if ((mode & 0xf0) == COUNT) {
                if (giKwidechan == 0) {
                    count[uhSysch]++;
                } else {
                    iii = 0;
                    if (giNwidechan > 0) {
                        for (ia=0; ia<giNwidechan; ia++) {
                            if (uhWidech[ia] == uhSysch0) break;
                        }
                        if (ia < giNwidechan) {
                            (*(piCount[ia]+uhSysch))++;
                        } else {
                            if (giNwidechan < MAX_WIDECHAN) {
                                iii = 1;
                            } else {
                                printf("wide chan max over. (%04x)\n", uhSysch0);
                                exit(0);
                            }
                        }
                    } else {
                        iii = 1;
                    }
                    if (iii == 1) {
                        piCount[giNwidechan] = malloc(65536*sizeof(int));
                        if (piCount[giNwidechan] == NULL) {
                            printf("malloc error for %04x\n", uhSysch0);
                            exit(0);
                        } else {
                            (*(piCount[giNwidechan]+uhSysch))++;
                            uhWidech[giNwidechan] = uhSysch0;
                            giNwidechan++;
                        }
                    }
                }
            }
            if ((mode & 0x0f) == MON) {
                gs = 2;
                for (i = 0; i < SR_MON; i++) {
                    j = (pucPtr[gs] & 0x03) * 2;
                    gs += j + 1;
                    if (j == 0)
                        gs++;
                }
                if ((mode & 0xf0) == 0 && sec == ss) {
                    printf("%4d : ch %04X    %3d Hz  %4d B\n", nch + 1, uhSysch, SR_MON, gs);
                }
            } else {
                if ((pucPtr[2] & 0x80) == 0) {     /* channel header = 4
                                                 * byte */
                    sr = pucPtr[3] + (((int) (pucPtr[2] & 0x0f)) << 8);
                    size = (pucPtr[2] >> 4) & 0x7;  /** offset size (0---4) **/
                    if (size) {
                        gs = size * (sr - 1) + 8;
                    } else {
                        gs = (sr >> 1) + 8;
                    }
#if DEBUG
                    printf("gs=%d gh=%02x%02x%02x%02x%02x sr=%d gs=%d pucPtr=%08x pucPtr_lim=%08x\n",
                        gs, pucPtr[0], pucPtr[1], pucPtr[2], pucPtr[3], pucPtr[4], sr, gs, pucPtr, pucPtr_lim);
#endif
                    if ((mode & 0xf0) == 0 && sec == ss) {
                        switch (size) {
                        case 0:
                            strcpy(cBytes, "0.5");
                            break;
                        case 1:
                            strcpy(cBytes, "1  ");
                            break;
                        case 2:
                            strcpy(cBytes, "2  ");
                            break;
                        case 3:
                            strcpy(cBytes, "3  ");
                            break;
                        case 4:
                            strcpy(cBytes, "4  ");
                            break;
                        default:
                            strcpy(cBytes, "  ?");
                            break;
                        }
                        if (giKwin32 == 0) {
                            printf("%4d : ch %04X    %3d Hz  x  %s B  = %4d B\n",
                                nch + 1, uhSysch, sr, cBytes, gs);
                        } else {
                            if (giKwidechan == 0) {
                                printf("%4d : ch %04X    %3d Hz  x  %s B  = %4d B\n",
                                    nch + 1, uhSysch, sr, cBytes, gs+2);
                            } else {
                                printf("%4d : ch %04X%04X    %3d Hz  x  %s B  = %4d B\n",
                                    nch + 1, uhSysch0, uhSysch, sr, cBytes, gs+2);
                                kkkkkk++;
                            }
                        }
                    }
                } else {
                    if ((mode & 0x0f) == RAW_HSR) {     /* channel header = 5
                                                         * byte */
                        sr = pucPtr[4] + (((int) pucPtr[3]) << 8) + (((int) (pucPtr[2] & 0x0f)) << 16);
                        size = (pucPtr[2] >> 4) & 0x7;
                        if (size)
                            gs = size * (sr - 1) + 8;
                        else
                            gs = (sr >> 1) + 8;
                        gs++;
                        if ((mode & 0xf0) == 0 && sec == ss) {
                            switch (size) {
                            case 0:
                                strcpy(cBytes, "0.5");
                                break;
                            case 1:
                                strcpy(cBytes, "1  ");
                                break;
                            case 2:
                                strcpy(cBytes, "2  ");
                                break;
                            case 3:
                                strcpy(cBytes, "3  ");
                                break;
                            case 4:
                                strcpy(cBytes, "4  ");
                                break;
                            default:
                                strcpy(cBytes, "  ?");
                                break;
                            }
                            printf("%4d : ch %04X    %3d Hz  x  %s B  = %4d B\n",
                                nch + 1, uhSysch, sr, cBytes, gs);
                        }
                    } else {            /* WIN2 format */
                        sr = pucPtr[3] + (((int) (pucPtr[2] & 0x03)) << 8);
                        size = ((pucPtr[2] >> 2) & 0x1F) + 1;      /* in bits */
                        gs = ((sr - 1) * size - 1) / 8 + 1 + 8;
                        if ((mode & 0xf0) == 0 && sec == ss)
                            printf("%4d : ch %04X    %3d Hz  x  %2d b  = %4d B\n",
                                nch + 1, uhSysch, sr, size, gs);
                    }
                }
            }
            if (giKwin32 == 0) {
                pucPtr += gs;
            } else {
                pucPtr += gs+2;
            }
            nch++;
            if (giKwin32 == 0) {
                pucPtr0 = pucPtr;
            } else {
                pucPtr0 = pucPtr-2;
            }
        } while (pucPtr < pucPtr_lim);
        if ((mode & 0xf0) == 0) {
            if (sec == ss) {
                printf("\n");
            }
            if (giKwin32 == 0) {
                printf("%4d : %02x%02x%02x %02x%02x%02x", sec + 1, pucMainbuf[4],
                    pucMainbuf[5], pucMainbuf[6], pucMainbuf[7], pucMainbuf[8], pucMainbuf[9]);
                printf("   %d ch  (%d bytes)\n", nch, iMainsize);
            } else {
                memmove(&iFlen, &pucMainbuf[12], 4);
                iFlen = IntFromBigEndian(iFlen);
                printf("%4d : %02x%02x%02x%02x %02x%02x%02x%02x (%02d)", sec + 1, pucMainbuf[4],
                    pucMainbuf[5], pucMainbuf[6], pucMainbuf[7], pucMainbuf[8], pucMainbuf[9],
                    pucMainbuf[10], pucMainbuf[11], iFlen);
                printf("   %d ch  (%d bytes)\n", nch, iMainsize);
            }
        }
        ts += iMainsize;
        sec++;
    }
    if ((mode & 0xf0) == 0) {
        if (giKwin32 == 0) {
            printf("\nlength = %d s  (%d bytes)\n\n", sec, ts);
        } else {
            printf("\nlength = %d s  (%d bytes)\n\n", sec, ts+4);
        }
    } else {
        if (giKwidechan == 0) {
            for (i = 0; i < 65536; i++) {
                if (count[i] > 0) {
                    printf("%04X %d\n", i, count[i]);
                }
            }
        } else {
            for (i=0; i<giNwidechan; i++) {
                for (ia=0; ia<65536; ia++) {
                    if (*(piCount[i]+ia) > 0) {
                        printf("%04x%04X %d\n", uhWidech[i], ia, *(piCount[i]+ia));
                    }
                }
            }
        }
    }
    exit(0);
}

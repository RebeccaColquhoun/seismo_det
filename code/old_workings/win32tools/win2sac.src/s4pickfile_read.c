#include <time.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <s4win2sac.h>
extern char cFileprm[1024];
extern int  giKwin32;
extern int  giKwidechan;
int 
pickfile_read(
    unsigned int uiSysch,                         /** ( I ) チャネル番号 (例： 4a63 ) **/
    char cWinfile[],                    /** ( I ) WINファイル名（ディレクトリー部をのぞく） **/
    int *iNzyear,
    int *iNzjday,
    int *iNzhour,
    int *iNzmin,
    int *iNzsec,
    float *fO,       /** 発振時刻が波形ファイルの先頭時刻から何秒後か **/
    float *fStla,
    float *fStlo,
    float *fStel,
    float *fEvla,    /** #f No.1 card 8 col.(latitude) **/
    float *fEvlo,    /** #f No.1 card 9 col.(longitude) **/
    float *fEvdp,    /** #f No.1 card 10 col.(depth) **/
    float *fDist,
    float *fAz,      /** #f No.2 card 4 col.(震央距離) **/
    float *fA,       /** #s 4 col.(P-time) **/
    float *fT9,      /** #s 6 col.(S-time) **/
    char *pcUD,      /** #s 3 col.(初動極性) **/
    char *pcUNE      /** チャンネルテーブルの成分コード **/
)
{
    struct tm stTm;
    struct tm *pstTm1;
    time_t  stTime1;  /** 波形ファイルの先頭時刻 **/
    time_t  stTime2;  /** 発振時刻 **/
    time_t  stTime3;
    DIR    *dirp;
    struct dirent *dp;
    struct stat st;
    int     iNsharps;
    int     iYears = 0;
    int     iMonths = 0;
    int     iDays = 0;
    int     iHours = 0;
    int     iMinutes = 0;
    int     iRet;
    int     ia;
    int     iFnum;
    int     iShsw;
    int     iFhsw;
    int     iFsw = 0;
    int     iSsw = 0;
    int     iEr;
    int     iKer;
    int     iSw;
    unsigned int     iChanno;
    int     iKexist;
    int     iYear;
    int     iYearf;
    int     iMonth;
    int     iMonthf;
    int     iDay;
    int     iDayf;
    int     iHour;
    int     iHourf;
    int     iMinute;
    int     iMinutef;
    int     iSec;
    int     iSecf;
    float   fSecf;
    char   *pc;
    char    cStname[8];
    char    cBuff[1000];
    char    cWrk1[1000];
    char    cWrk2[1000];
    char    cWrk3[1000];
    char    cWrk4[1000];
    char    cWrk5[1000];
    char    c1[100];
    char    c2[100];
    char    c3[100];
    char    c4[100];
    char    c5[100];
    char    c6[100];
    char    c7[100];
    char    c8[100];
    char    c9[100];
    char    c10[100];
    char    c11[100];
    char    c12[100];
    static FILE   *psFile = NULL;
    char    cChtblname[1000];
    char    cPicdirname[1000];
    iRet = 1;
    iFhsw = 0;
    iShsw = 0;
    /** ディフォルト設定 **/
    *fO = -12345.0;
    *fEvla = -12345.0;
    *fEvlo = -12345.0;
    *fEvdp = -12345.0;
    *fStla = -12345.0;
    *fStlo = -12345.0;
    *fStel = -12345.0;
    pcUD[0] = '\0';
    *fA = -12345.0;
    *fT9 = -12345.0;
    *fDist = -12345.0;
    *fAz = -12345.0;
    /** win.prm ファイル読み込み **/
    if (psFile != (FILE *) NULL) {
        fprintf(stderr,"***** warning ***** win.prm file not close error.(%s)\n", cFileprm);
        exit (0);
    }
    psFile = fopen(cFileprm, "r");
    if (psFile == (FILE *) NULL) {
        fprintf(stderr,"***** warning ***** win.prm file not found.(%s)\n", cFileprm);
        goto ret;
    }
    for (ia = 0; ia < 4; ia++) {
        pc = fgets(cBuff, 1000, psFile);
        if (pc == NULL) {
            fprintf(stderr,"***** warning ***** win.prm file read error.\n");
            goto ret;
        }
        if (ia == 1) {
            sscanf(cBuff, "%s", cChtblname);
        }
        if (ia == 3) {
            sscanf(cBuff, "%s", cPicdirname);
        }
    }
    if (psFile != (FILE *) NULL) {
        fclose(psFile);
        psFile = NULL;
    }
    /** チャネルテーブルファイルを読み込む **/
    if (psFile != (FILE *) NULL) {
        fprintf(stderr,"***** error ***** channel table file not close error.(%s)\n", cChtblname);
        exit (0);
    }
    psFile = fopen(cChtblname, "r");
    if (psFile == (FILE *) NULL) {
        fprintf(stderr,"***** warning ***** channel table file read error.(%s)\n", cChtblname);
        exit(0);
    }
    iSw = 0;
    while ((pc = fgets(cBuff, 1000, psFile)) != NULL) {
        if (cBuff[0] == '#')
            continue;
        sscanf(cBuff, "%s %s %s %s %s", cWrk1, cWrk2, cWrk3, cWrk4, cWrk5);
        iChanno = strtoul(cWrk1, (char **) NULL, 16);
        uiSysch = 0x0000ffff & uiSysch;
        if (iChanno == uiSysch) {
            iSw = 1;
            break;
        }
    }
    if (psFile != (FILE *) NULL) {
        fclose(psFile);
        psFile = (FILE *) NULL;
    }
    if (iSw == 0) {
        if (giKwidechan == 0) {
            fprintf(stderr,"Channel not found in channel table.(%04x)\n", uiSysch);
        } else {
            fprintf(stderr,"Channel not found in channel table.(%08x)\n", uiSysch);
        }
        goto ret;
    }
    if (strlen(cWrk4) > 7) {
        fprintf(stderr,"***** ERROR ***** The number of station name length is illegal(max. 7).(%s)\n", cWrk4);
        exit (0);
    }
    strcpy(cStname, cWrk4);
    if (strlen(cWrk5) > 7) {
        fprintf(stderr,"***** ERROR ***** The number of UNE code length is illegal(max. 7).(%s)\n", cWrk5);
        exit (0);
    }
    strcpy(pcUNE, cWrk5);
    /** search PIC file **/
    iSw = 0;
    if (cPicdirname[strlen(cPicdirname)-1] == '/') {
        if (giKwin32 == 1) {
            strncat(cPicdirname, &cWinfile[2], 4);
        } else {
            strncat(cPicdirname, cWinfile, 4);
        }
    }
    strcat(cPicdirname, "/");
    dirp = opendir(cPicdirname);
    if (dirp == (DIR *) NULL) {
        fprintf(stderr,"***** warning ***** Directry not found.(%s)\n", cPicdirname);
        goto ret;
    }
    iKexist = 0;
    iEr = 0;
    while ((dp = readdir(dirp)) != NULL) {
        if ((int) strlen(dp->d_name) != 17)
            continue;
        if (*(dp->d_name + 6) != '.')
            continue;
        if (*(dp->d_name + 13) != '.')
            continue;
        strcpy(cWrk1, cPicdirname);
        strcat(cWrk1, dp->d_name);
        if (stat(cWrk1, &st) == 0 && (st.st_mode & S_IFMT) == S_IFREG) {
            if (psFile != (FILE *) NULL) {
                fclose(psFile);
                psFile = (FILE *) NULL;
            }
            psFile = fopen(cWrk1, "r");
            if (psFile == (FILE *) NULL)
                continue;
            pc = fgets(cBuff, 1000, psFile);
            if (pc == (char *) NULL)
                continue;
            sscanf(cBuff, "%s %s", cWrk2, cWrk3);
            if (strncmp(cWrk2, "#p", 2) != 0)
                continue;
            if (strcmp(cWrk3, cWinfile) != 0)
                continue;
            iKexist = 1;
            iEr = 1;
            pc = fgets(cBuff, 1000, psFile);
            if (pc == (char *) NULL)
                break;
            iKer = sscanf(cBuff, "%s %d %d %d %d %d %d",
                cWrk2, &iYear, &iMonth, &iDay, &iHour, &iMinute, &iSec); /** 波形ファイルの先頭時刻 */
            if (iKer != 7)
                break;
            if (strcmp(cWrk2, "#p") != 0)
                break;
            iFnum = 0;
            iSsw = 0;
            iFsw = 0;
            iNsharps = 0;
            while ((pc = fgets(cBuff, 1000, psFile)) != (char *) NULL) {
                iKer = sscanf(cBuff, "%s", cWrk2);
                if (iKer != 1)
                    continue;
                if (strcmp(cWrk2, "#s") == 0) { /** #s データ **/
                    iNsharps++;
                    if (iNsharps == 1) {
                        memmove(c1, &cBuff[3], 2);
                        c1[2] = '\0';
                        iYears = atoi(c1);
                        memmove(c1, &cBuff[6], 2);
                        c1[2] = '\0';
                        iMonths = atoi(c1);
                        memmove(c1, &cBuff[9], 2);
                        c1[2] = '\0';
                        iDays = atoi(c1);
                        memmove(c1, &cBuff[12], 2);
                        c1[2] = '\0';
                        iHours = atoi(c1);
                        memmove(c1, &cBuff[15], 2);
                        c1[2] = '\0';
                        iMinutes = atoi(c1);
                        iShsw = 1;
                    }
                    if (iSsw == 1)
                        continue;
                    iKer = sscanf(cBuff, "%s %s %s %s %s %s %s %s %s %s %s %s",
                                   c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12);
                    if (iKer != 12)
                        continue;
                    /** 観測点コードが異なるものは無視 **/
                    if (strcmp(c2, cStname) != 0)
                        continue;
                    /** **/
/*                     memmove(c1, &cBuff[52], 11); */
/*                     c1[11] = '\0'; */
/*                     *fStla = atof(c1); */
                    *fStla = atof(c10);
                    /** **/
/*                     memmove(c1, &cBuff[63], 11); */
/*                     c1[11] = '\0'; */
/*                     *fStlo = atof(c1); */
                    *fStlo = atof(c11);
                    /** **/
/*                     memmove(c1, &cBuff[74], 7); */
/*                     c1[7] = '\0'; */
/*                     *fStel = atof(c1); */
                    *fStel = atof(c12);
                    /** 初動極性 **/
/*                     memmove(pcUD, &cBuff[8], 1); */
/*                     pcUD[1] = '\0'; */
                    memmove(pcUD, c3, 1);
                    pcUD[1] = '\0';
                    /** Ｐ波到着秒 **/
/*                     memmove(c1, &cBuff[9], 8); */
/*                     c1[8] = '\0'; */
/*                     *fA = atof(c1); */
                    *fA = atof(c4);
                    /** Ｓ波到着秒 **/
/*                     memmove(c1, &cBuff[23], 8); */
/*                     c1[8] = '\0'; */
/*                     *fT9 = atof(c1); */
                    *fT9 = atof(c6);
                    iSsw = 1;
                    if (iFsw == 1)
                        break;
                } else if (strcmp(cWrk2, "#f") == 0) {
                    iFnum++;
                    if (iFnum == 1) {   /** #f データの１枚目 **/
                        iKer = sscanf(cBuff, "%s %d %d %d %d %d %f %f %f %f",
                            c1, &iYearf, &iMonthf, &iDayf, &iHourf, &iMinutef, &fSecf,
                            fEvla, fEvlo, fEvdp);
                        if (iKer != 10)
                            break;
                        iFhsw = 1;
                    } else {            /** #f データの２枚目以降 **/
/*                         iKer = sscanf(cBuff, "%2s %4s", c1, c2); */
/*                         if (iKer != 2) */
/*                             continue; */
                        iKer = sscanf(cBuff, "%s %s %s %s %s %s %s %s %s %s %s %s",
                                       c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12);
                        if (iKer != 12)
                            continue;  
                        if (strcmp(c2, cStname) != 0)
                            continue;
                        *fAz = atof(c4);
                        iFsw = 1;
                        if (iSsw == 1)
                            break;
                    }
                } else {
                    continue;
                }
            }
            if (psFile != (FILE *) NULL) {
                fclose(psFile);
                psFile = (FILE *) NULL;
            }
            if (iSsw != 1 || iFsw != 1)
                continue;
            iEr = 0;
            break;
        }
        if (iKexist == 1)
            break;
    }
    closedir(dirp);
    if (psFile != (FILE *) NULL) {
        fclose(psFile);
        psFile = (FILE *) NULL;
    }
    if (iKexist == 0) {
        fprintf(stderr,"***** warning ***** pick file not found.(%s)\n", cWinfile);
        goto ret;
    }
    /** all #s nothing **/
    if (iShsw == 0) {
        if (giKwidechan == 0) {
            fprintf(stderr,"***** warning ***** all #s data nothing in picks file. (channel=%04x)\n", uiSysch);
        } else {
            fprintf(stderr,"***** warning ***** all #s data nothing in picks file. (channel=%08x)\n", uiSysch);
        }
        goto ret;
    }
    if (iSsw == 0) {
        if (giKwidechan == 0) {
            fprintf(stderr,"***** warning ***** #s data nothing in picks file. (channel=%04x)\n", uiSysch);
        } else {
            fprintf(stderr,"***** warning ***** #s data nothing in picks file. (channel=%08x)\n", uiSysch);
        }
    }
    if (iFsw == 0) {
        if (giKwidechan == 0) {
            fprintf(stderr,"***** warning ***** #f data nothing in picks file. (channel=%04x)\n", uiSysch);
        } else {
            fprintf(stderr,"***** warning ***** #f data nothing in picks file. (channel=%08x)\n", uiSysch);
        }
    }
    /** 構造体に格納 **/
    if (iYear > 50) {
        iYear += 1900;
    } else {
        iYear += 2000;
    }
    stTm.tm_year = iYear - 1900;
    stTm.tm_mon = iMonth - 1;           /**  - 1 **/
    stTm.tm_mday = iDay;
    stTm.tm_hour = iHour;
    stTm.tm_min = iMinute;
    stTm.tm_sec = iSec;
    stTm.tm_sec = 0;
    stTm.tm_wday = 0;
    stTm.tm_yday = 0;
    stTm.tm_isdst = 0;
    stTime1 = mktime(&stTm); /** 波形ファイルの先頭時刻 **/
    pstTm1 = localtime(&stTime1);
    *iNzyear = pstTm1->tm_year + 1900;
    *iNzjday = pstTm1->tm_yday + 1;
    *iNzhour = pstTm1->tm_hour;
    *iNzmin = pstTm1->tm_min;
    *iNzsec = pstTm1->tm_sec;
    /** #f time **/
    if (iFhsw == 1) {
        if (iYearf > 50) {
            iYearf += 1900;
        } else {
            iYearf += 2000;
        }
        stTm.tm_year = iYearf - 1900;
        stTm.tm_mon = iMonthf - 1;      /**  - 1 **/
        stTm.tm_mday = iDayf;
        stTm.tm_hour = iHourf;
        stTm.tm_min = iMinutef;
        iSecf = fSecf;
        stTm.tm_sec = iSecf;
        fSecf = fSecf - (float) iSecf;
        stTm.tm_wday = 0;
        stTm.tm_yday = 0;
        stTm.tm_isdst = 0;
        stTime2 = mktime(&stTm); /** 発振時刻 **/
        pstTm1 = localtime(&stTime2);
        *fO = stTime2 - stTime1 + fSecf; /** 発振時刻が波形ファイルの先頭時刻から何秒後か **/
    }
    /** #s time **/
    if (iYears > 50) {
        iYears += 1900;
    } else {
        iYears += 2000;
    }
    stTm.tm_year = iYears - 1900;
    stTm.tm_mon = iMonths - 1;          /**  - 1 **/
    stTm.tm_mday = iDays;
    stTm.tm_hour = iHours;
    stTm.tm_min = iMinutes;
    stTm.tm_sec = 0;
    stTm.tm_wday = 0;
    stTm.tm_yday = 0;
    stTm.tm_isdst = 0;
    stTime3 = mktime(&stTm);  /** 基準年月日時分 **/
                              /** stTime1 = 波形ファイルの先頭時刻 **/
    if (iSsw == 1) {
        if (fabs(*fA) > 0.000005) {
            *fA += stTime3 - stTime1;  /** 波形ファイルの先頭時刻からのＰ−time **/
        } else {
            *fA = -12345.0;
        }
        if (fabs(*fT9) > 0.000005) {
            *fT9 += stTime3 - stTime1;  /** 波形ファイルの先頭時刻からのＳ−time **/
        } else {
            *fT9 = -12345.0;
        }
    }
    iRet = 0;
ret:;
    return iRet;
}

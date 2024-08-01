#include <s4win2sac.h>
#include <stdio.h>
#include <string.h>
#include <s4win2sac.h>
extern char cFileprm[1024];
extern char winfile[BUFSIZ];
extern char winfiled[BUFSIZ];
extern char sacfile[BUFSIZ];
extern _sac_header sac_header;
/*
################# stfind.c ###################
*/
#include  <ctype.h>
#include  <math.h>
#define  CHCODE  "./channels.tbl"
#define  DEBUG2 1
/* input station code and find station name and component  */
char    sunit[10];
extern unsigned char    gcOrganize2;
int 
stfind(unsigned int sysch, char kstnm[MAX_STATIONNAME+1], char kcmp[MAX_SEIBUNCODE+1], float *cmpaz,
    float *cmpinc, float *stla, float *stlo, float *stel, float *sense)
{
    int ii1;
    int ii2;
    int ii3;
    int iRet;
    static FILE   *fp = NULL;
    char    ss[300], chcode[BUFSIZ];
    char    cBuff[1000];
    unsigned int     num;
    float   vu;
    int     gain;
    float   adc;
    char   *pc;
    char   *pcs;
    int     ia;
    char    ssww[18][100];
    sprintf(chcode, "%s.ch", winfiled);
    /** win.prm ファイル読み込み **/
    if (fp != (FILE *) NULL) {
        fprintf(stderr,"***** error ***** win.prm file not close error.(%s)\n", cFileprm);
        exit(1);
    }
    fp = fopen(cFileprm, "r");
    if (fp == (FILE *) NULL) {
        fprintf(stderr,"***** error ***** win.prm file not found.(%s)\n", cFileprm);
        exit(1);
    }
    pc = fgets(cBuff, 1000, fp);
    if (pc == NULL) {
        fprintf(stderr,"***** error ***** win.prm file read error.\n");
        exit(1);
    }
    pc = fgets(cBuff, 1000, fp);
    if (pc == NULL) {
        fprintf(stderr,"***** error ***** win.prm file read error.\n");
        exit(1);
    }
    sscanf(cBuff, "%s", chcode);
    fclose(fp);
    fp = fopen(chcode, "r");
    if (fp == NULL) {
        fprintf(stderr,"***** error ***** Channel file %s not found.\n", chcode);
        exit(1);
    }
    while (fgets(ss, 200, fp) != NULL) {
        ss[(int) strlen(ss) - 1] = (char) NULL;
        if ((int) strlen(ss) > 0 && ss[0] != '#') {
            pcs = &ss[0];
            for (ia = 0; ia < 18; ia++) {
                ssww[ia][0] = (char) NULL;
            }
            for (ia = 0; ia < 18; ia++) {
                pc = strtok(pcs, " \t");
                if (pc == (char *) NULL) break;
                if (GS_NUMBER(ssww[ia]) <= strlen(pc)) {
                    printf("***** ERROR ***** The number of letter is too long.(%s)(%s %d).\n",
                              pc, __FILE__, __LINE__);
                    exit (0);
                }
                strcpy(ssww[ia], pc);
                pcs = NULL;
            }
            if (ia == 0) continue;
            for (ia = 0; ia < 18; ia++) {
            }
            if (ssww[13][0] != (char) NULL)
                sscanf(ssww[13], "%f", stla);
            if (ssww[14][0] != (char) NULL)
                sscanf(ssww[14], "%f", stlo);
            if (ssww[15][0] != (char) NULL)
                sscanf(ssww[15], "%f", stel);
            sscanf(ssww[0], "%x", &num);
            sysch = sysch & 0x0000ffff;
            if (sysch == num) {
                if (ssww[3][0] != (char) NULL) {
                    ii1 = MAX_STATIONNAME+1;
                    ii2 = strlen(ssww[3]);
                    ii3 = GS_MIN(ii1-1, ii2);
                    memset(kstnm, (int)NULL, ii1);
                    strncpy(kstnm, ssww[3], ii3);
/**                    sscanf(ssww[3], "%s", kstnm); **/
                }
                if (ssww[4][0] != (char) NULL) {
                    ii1 = MAX_SEIBUNCODE+1;
                    ii2 = strlen(ssww[4]);
                    ii3 = GS_MIN(ii1-1, ii2);
                    memset(kcmp, (int)NULL, ii1);
                    strncpy(kcmp, ssww[4], ii3);
/**                    sscanf(ssww[4], "%s", kcmp); **/
                }
                if (ssww[7][0] != (char) NULL) {
                    sscanf(ssww[7], "%f", &vu);
                }
                if (ssww[8][0] != (char) NULL) {
                    ii1 = GS_NUMBER(sunit);
                    ii2 = strlen(ssww[8]);
                    ii3 = GS_MIN(ii1-1, ii2);
                    memset(sunit, (int)NULL, ii1);
                    strncpy(sunit, ssww[8], ii3);
/**                    sscanf(ssww[8], "%s", sunit); **/
                }
                if (ssww[11][0] != (char) NULL) {
                    sscanf(ssww[11], "%d", &gain);
                }
                if (ssww[12][0] != (char) NULL) {
                    sscanf(ssww[12], "%f", &adc);
                }
                *sense = (adc / (float) pow(10.0, (double) gain / 20.0)) / (float) vu;
                ii1 = GS_NUMBER(sac_header.kcmpnm);
                ii2 = strlen(kcmp);
                ii3 = GS_MIN(ii1-1, ii2);
                memset(sac_header.kcmpnm, (int)NULL, ii1);
                strncpy(sac_header.kcmpnm, kcmp, ii3);
/**                strcpy(sac_header.kcmpnm, kcmp); **/
                if (!(kcmp[0] == 'w' || kcmp[0] == 'L' || kcmp[0] == 'H' || kcmp[0] == 'B')) {
                    switch (kcmp[0]) {
                    case 'U':
                    case 'Z':
                        *cmpaz = 0.0;
                        *cmpinc = 0.0;
                        break;
                    case 'V':
                        *cmpaz = 0.0;
                        *cmpinc = 0.0;
                        break;
                    case 'D':
                        *cmpaz = 0.0;
                        *cmpinc = 180.0;
                        break;
                    case 'N':
                    case 'Y':
                        *cmpaz = 0.0;
                        *cmpinc = 90.0;
                        break;
                    case 'S':
                        *cmpaz = 180.0;
                        *cmpinc = 90.0;
                        break;
                    case 'E':
                    case 'X':
                        *cmpaz = 90.0;
                        *cmpinc = 90.0;
                        break;
                    case 'W':
                        *cmpaz = -90.0;
                        *cmpinc = 90.0;
                        break;
                    default:
                        *cmpaz = -12345;
                        *cmpinc = -12345;
                        break;
                    }
                } else {
                    switch (kcmp[1]) {
                    case 'U':
                    case 'Z':
                        *cmpaz = 0.0;
                        *cmpinc = 0.0;
                        break;
                    case 'V':
                        *cmpaz = 0.0;
                        *cmpinc = 0.0;
                        break;
                    case 'N':
                    case 'Y':
                        *cmpaz = 0.0;
                        *cmpinc = 90.0;
                        break;
                    case 'E':
                    case 'X':
                        *cmpaz = 90.0;
                        *cmpinc = 90.0;
                        break;
                    default:
                        *cmpaz = -12345;
                        *cmpinc = -12345;
                        break;
                    }
                }
                iRet = 1;
                goto ret;
            }
        }
    }
    fclose(fp);
    fp = NULL;
    iRet = -1;
ret:;
    if (fp != NULL) {
        fclose(fp);
        fp = NULL;
    }
    return (iRet);
}

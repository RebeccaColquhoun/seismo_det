#ifndef WIN2SAC__HHH
#define WIN2SAC__HHH

#include <stdio.h>
#include <stdlib.h>
#define GS_MIN(a,b) (((a)<(b))?(a):(b)) /** 最小値 **/
#define GS_MAX(a,b) (((a)>(b))?(a):(b)) /** 最大値 **/
#define GS_NUMBER(arr)       ((int) (sizeof(arr) / sizeof(arr[0])))     /** 配列の大きさ **/
#define MAX_STATIONNAME 16
#define MAX_SEIBUNCODE  16

typedef struct {
    float   delta;
    float   depmin, depmax;
    float   scale;
    float   odelta;
    float   b, e, o, a;
    float   rint1;
    float   t0, t1, t2, t3, t4, t5, t6, t7, t8, t9;
    float   f;
    float   resp0, resp1, resp2, resp3, resp4;
    float   resp5, resp6, resp7, resp8, resp9;
    float   stla, stlo, stel, stdp;
    float   evla, evlo, evel, evdp;
    float   runs1;
    float   user0, user1, user2, user3, user4;
    float   user5, user6, user7, user8, user9;
    float   dist, az, baz, gcarc;
    float   rint2, rint3;
    float   depmen, cmpaz, cmpinc;
    float   runs2[11];  /* 70 words (280 byte) */

    int     nzyear, nzjday, nzhour, nzmin, nzsec;
    int     nzmsec, nvhdr;
    int     iint1[2];
    int     npts;
    int     iint2[2], iuns1[3];
    int     iftype, idep, iztype;
    int     iuns2;
    int     iinst, istreg, ievreg, ievtyp, iqual, isynth;
    int     iuns3[10];

    int     leven, lpspol, lovrok, lcalda;
    int     luns1;  /* 110 words (440 byte) */

    char    kstnm[8], kevnm[16];
    char    khole[8], ko[8], ka[8];
    char    kt0[8], kt1[8], kt2[8], kt3[8], kt4[8];
    char    kt5[8], kt6[8], kt7[8], kt8[8], kt9[8];
    char    kf[8];
    char    kuser0[8], kuser1[8], kuser2[8];
    char    kcmpnm[8], knetwk[8], kdatrd[8], kinst[8];
}       _sac_header;

typedef struct {
    float   rvar[70];
    int     ivar[35];
    int     lvar[5];
    char    cvar[24][8];
}       _sac_hdr2;


extern void adj_time(int *tm);
extern void bcd_dec(int *dest, char *sour);
extern int day_of_year(int year, int month, int day);
extern unsigned int mkint(unsigned char *ptr);
extern void month_day(int year, int yearday, int *pmonth, int *pday);
extern void newhdr(void);
extern int read_data(unsigned char **ptr, FILE * fp);
extern int read_one_sec(unsigned char *ptr, unsigned int sys_ch, int *abuf);
extern int 
stfind(unsigned int chno, char kstnm[MAX_STATIONNAME+1], char kcmp[MAX_SEIBUNCODE+1], float *cmpaz,
    float *cmpinc, float *stla, float *stlo, float *stel, float *sense);
extern int time_cmp(int *t1, int *t2);
extern int win2sac0(int npts, int srate, unsigned int sysch, int *toptm);
extern int main(int argc, char *argv[]);
extern void bytrev_(unsigned char *puc1, int *piByte);
extern int 
pickfile_read(
    unsigned int iSysch,                         /** ( I ) チャネル番号 (例： 4a63 ) **/
    char cWinfile[],                    /** ( I ) WINファイル名（ディレクトリー部をのぞく） **/
    int *iNzyear,
    int *iNzjday,
    int *iNzhour,
    int *iNzmin,
    int *iNzsec,
    float *fO,
    float *fStla,
    float *fStlo,
    float *fStel,
    float *fEvla,
    float *fEvlo,
    float *fEvdp,
    float *fDist,
    float *fAz,
    float *fA,
    float *fT0,
    char *pcUD,
    char *pcUNE
);
extern void swap4b(unsigned int *pic);
extern void swap2b(unsigned short int *pic);
extern void swap_header(_sac_header * ptHeader);

#endif

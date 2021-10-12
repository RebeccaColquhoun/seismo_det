#ifndef __V9DEWIN__PROT__H
#define __V9DEWIN__PROT__H
#include <stdio.h>

#define MAX_FILT    100
struct Filter {
    char    kind[12];
    double  fl, fh, fp, fs, ap, as;
    int     m_filt;                     /* order of filter */
    int     n_filt;                     /* order of Butterworth
                                         * function */
    double  coef[MAX_FILT * 4];         /* filter coefficients */
    double  gn_filt;                    /* gain factor of filter */
};

extern int adj_time(int *tm);
extern void ctrlc(int iii);
extern void adj_time2(int *time);
extern int bcd_dec(int * dest, char * sour);
extern void bcd_dec8(int    *dest, char   *sour);
extern int buthip(double *h, int    * m, double * gn, int * n, double fp, double fs, double ap, double as);
extern int butlop(double * h, int * m, double * gn, int * n, double fp, double fs, double ap, double as);
extern int butpas(double * h, int * m, double * gn, int * n, double fl, double fh, double fs, double ap, double as);
extern unsigned int cvt(int ch);
extern int get_filter(int sr, struct Filter * f);
extern int mkint(unsigned char * ptr);
extern int print_usage(void);
extern int read_data(unsigned char **ptr, FILE *fp);
extern int read_one_sec(
    unsigned char *ptr,                 /* input */
    unsigned int sys_ch,                        /* sys_ch = sys*256 + ch */
    int *abuf                          /* output */
);
extern int recfil(double * x, double * y, int n, double * h, int nml, double * uv);
extern int tandem(double * x, double * y, int n, double * h, int m, int nml, double * uv);
extern int time_cmp(int * t1, int * t2, int i);
extern void swap4b(unsigned int *pic);
extern void swap2b(unsigned short *pic);
extern int get_channel(char * pcParameter, int  * piNchannel, unsigned int **ppuhChid);
extern void blkcut( char *pcOut, char *pcIn);

#endif

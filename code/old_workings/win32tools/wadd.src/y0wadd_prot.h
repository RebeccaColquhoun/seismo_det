#ifndef Y0WADD_PROT__HHH
#define Y0WADD_PROT__HHH

#include <stdio.h>

extern int adj_time(int * tm);
extern void check( int iSize, unsigned char * pucAdr);
extern void check2( int iSize, unsigned char * pucAdr);
extern int win2fix( unsigned char *pucPtr, int *piAbuf, unsigned short *puhChanno, int *piNsampno );
extern int adj_time_m(int * tm);
extern void bcd_dec(int *dest, char *sour);
extern int cptm(int * dst, int * src);
extern int elim_ch(unsigned int *sys_ch, int n_ch, unsigned char *old_buf, unsigned char *new_buf);
extern int get_sysch(unsigned char *buf, unsigned int *sys_ch);
extern int get_time(int * rt);
extern void make_skel(unsigned char *old_buf, unsigned char *new_buf);
extern int read_data_main(unsigned char *ptr, FILE   *fp);
extern int read_data_sub(unsigned char *ptr, FILE   *fp);
extern int form_write(FILE * f_out);
extern int strcmp2(char * s1, char * s2);
extern int strncmp2(char * s1, char * s2, int i);
extern int time_cmp(int * t1, int * t2, int i);
extern void swap4b(unsigned int *pic);
extern void swap2b(unsigned short int *pic);
extern int werror();

#endif  /** Y0WADD_PROT__HHH **/

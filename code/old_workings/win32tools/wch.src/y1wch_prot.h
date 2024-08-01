#ifndef __WCH__PROT__H
#define __WCH__PROT__H
#include <stdio.h>

extern void swap4b(unsigned int *pic);

extern void ctrlc(int iii);

extern int form_write(FILE * f_out);

extern void get_one_record(void);

extern int mkint(unsigned char * ptr);

extern unsigned short mkshort(unsigned char * ptr);

extern int read_chfile(char   * chfile);

extern int read_data(void);
extern int select_ch(unsigned char *table, unsigned char *old_buf, unsigned char *new_buf);
extern int strcmp2(char   * s1, char   * s2);
extern int strncmp2(char * s1, char * s2, int i);

#endif

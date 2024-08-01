#ifndef __WCHCH__PROT__H
#define __WCHCH__PROT__H

extern void ctrlc(int iii);

extern int form_write(FILE * f_out);
extern void get_one_record(void);
extern int mkint(unsigned char * ptr);
extern int read_chfile(char * chfile);
extern int read_data(void);
extern int select_ch(unsigned int * table0, unsigned int * table1, unsigned char * old_buf, unsigned char * new_buf);
extern void swap4b(unsigned int *pic);

#endif

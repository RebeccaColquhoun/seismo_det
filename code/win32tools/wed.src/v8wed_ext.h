#ifndef WED_EXT_HHHH
#define WED_EXT_HHHH

#include    <stdio.h>
#include    <signal.h>

#define     DEBUG       0
#define     DEBUG1      0
#define MAX_WIDECHAN 100
#define MAX_CHANNUM 65536

#define IntFromBigEndian(a) \
  ((((unsigned char *)&(a))[0]<<24)+(((unsigned char *)&(a))[1]<<16)+ \
  (((unsigned char *)&(a))[2]<<8)+((unsigned char *)&(a))[3])
#define IntToBigEndian(a,b) \
   (b)[0]=a>>24; (b)[1]=a>>16; (b)[2]=a>>8; (b)[3]=a;


extern unsigned char *buf, *outbuf;
extern unsigned char *buf2;
extern int win2_blk_size;
extern int leng, dec_start[8], dec_end[8], dec_now[8], nch;
extern unsigned int guiSysch[MAX_CHANNUM];
extern FILE *f_param;

extern int select_ch(unsigned int *sys_ch, int n_ch, unsigned char *old_buf, unsigned char *new_buf);
extern void swap4b(unsigned int *pic);
extern void get_one_record(void);

#endif

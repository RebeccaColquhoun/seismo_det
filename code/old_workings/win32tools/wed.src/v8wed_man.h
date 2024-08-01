#ifndef WED_MAN_HHHH
#define WED_MAN_HHHH

#include    <stdio.h>
#include    <signal.h>

#define MAX_WIDECHAN 100
#define MAX_CHANNUM 65536

#define     DEBUG       0
#define     DEBUG1      0

#define IntFromBigEndian(a) \
  ((((unsigned char *)&(a))[0]<<24)+(((unsigned char *)&(a))[1]<<16)+ \
  (((unsigned char *)&(a))[2]<<8)+((unsigned char *)&(a))[3])
#define IntToBigEndian(a,b) \
   (b)[0]=a>>24; (b)[1]=a>>16; (b)[2]=a>>8; (b)[3]=a;


unsigned char *buf, *outbuf;
unsigned char *buf2;
int     win2_blk_size;
int     leng, dec_start[6], dec_end[6], dec_now[6], nch;
unsigned int guiSysch[MAX_CHANNUM];
FILE   *f_param;
extern void get_one_record(void);

#endif

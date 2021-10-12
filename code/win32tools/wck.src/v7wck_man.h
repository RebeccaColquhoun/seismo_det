#ifndef V7WCK_MAN_HHHH
#define V7WCK_MAN_HHHH
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>

#define DEBUG   0
#define DEBUG1  0
#define IntFromBigEndian(a) \
  ((((unsigned char *)&(a))[0]<<24)+(((unsigned char *)&(a))[1]<<16)+ \
  (((unsigned char *)&(a))[2]<<8)+((unsigned char *)&(a))[3])
int     count[65536];
#endif

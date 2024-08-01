#include <stdlib.h> 
#include <stdio.h> 
    
/*************************************************************************/
/* 1.関数名                   usage                                      */
/* 2.機能                                                                */
/*   wck プロセスの使い方を表示する。                          */
/* 3.構文及びパラメータ解説                                              */
/*   void usage(void);                           */
/* 4.戻り値                                                              */
/*   なし                              */
/*************************************************************************/
void
usage(void)
{
    fprintf(stderr, "Usage: wck_32 (-u/-?/-Y/-r/-m/-h/-c/-a) [-tTime] [-nNoch] [-s] ([data file]/- ([sec position]))\n");
    fprintf(stderr, "              -u         This usage print                                    \n");
    fprintf(stderr, "              -?         This usage print                                    \n");
    fprintf(stderr, "              -Y         wide chanel version                                 \n");
    fprintf(stderr, "              -r         RAW data                                            \n");
    fprintf(stderr, "              -m         MON data                                            \n");
    fprintf(stderr, "              -h         High sampling rate format RAW data                  \n");
    fprintf(stderr, "              -c         Count mode                                          \n");
    fprintf(stderr, "              -a         Sampling data all print (stderr)                    \n");
    fprintf(stderr, "                         Ignore -t & -n option                               \n");
    fprintf(stderr, "              -t         Time data print (stderr)                            \n");
    fprintf(stderr, "                         Time = YYMMDDhhmmss | YYYYMMDDhhmmss                \n");
    fprintf(stderr, "              -n         Channel data print (stderr)                         \n");
    fprintf(stderr, "                         Noch = channel no.(hex)                             \n");
    fprintf(stderr, "              -s         If data print, print raw data                       \n");
    fprintf(stderr, "       data file         win1 or win32 data file name                        \n");
    fprintf(stderr, "               -         stdin input                                         \n");
    fprintf(stderr, "    sec position         sec position                                        \n");
}

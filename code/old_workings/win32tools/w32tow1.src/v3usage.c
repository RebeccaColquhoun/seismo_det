#include <stdio.h> 
#include <stdlib.h> 
    
/*************************************************************************/
/* 1.関数名                   usage                                      */
/* 2.機能                                                                */
/*   w32tow1 プロセスの使い方を表示する。                          */
/* 3.構文及びパラメータ解説                                              */
/*   void usage(void);                           */
/* 4.戻り値                                                              */
/*   なし                              */
/*************************************************************************/
void
usage(void)
{
    fprintf(stderr, "Usage: w32tow1_32 [-s] [-h] [-?] Win32_file Win1_file                 \n");
    fprintf(stderr, "              -s         sort by date & channel no.                \n");
    fprintf(stderr, "              -h         This usage print                          \n");
    fprintf(stderr, "              -?         This usage print                          \n");
    fprintf(stderr, "      Win32_file         WIN32 format file name                    \n");
    fprintf(stderr, "       Win1_file         WIN1 format file name                     \n");
    fprintf(stderr, "                                                                   \n");
}

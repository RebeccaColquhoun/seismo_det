#include <stdio.h> 
#include <stdlib.h> 
    
/*************************************************************************/
/* 1.�ؿ�̾                   usage                                      */
/* 2.��ǽ                                                                */
/*   w32tow1 �ץ����λȤ�����ɽ�����롣                          */
/* 3.��ʸ�ڤӥѥ�᡼������                                              */
/*   void usage(void);                           */
/* 4.�����                                                              */
/*   �ʤ�                              */
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

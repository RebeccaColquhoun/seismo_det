#include <stdio.h>
#include <stdlib.h>
#include <s8c32_prot.h>
/******************************************************************************
 *
 * NAME        :c32usage
 * FUNCTION    :使用方法表示
 * PROCESS     :使用方法を表示する。
 * PROGRAMMED  :kjmatsu
 * DATE(ORG)   :2000.10.03
 * REMARKS     :備考
 *
 *****************************************************************************/
void
c32usage(
)
{
    fprintf(stderr, "USAGE :\n") ;
    fprintf(stderr, "  catwin32_32 File_1 File_2 ... File_n [-oOutFile | -o OutFile] [-s] [-h] [-?]\n") ;
    fprintf(stderr, "      File_n        : Input WIN32 file name\n");
    fprintf(stderr, "                    : You may use a wild word character. \n");
    fprintf(stderr, "      OutFile       : Output WIN32 file name\n");
    fprintf(stderr, "      -s            : Sort by date & channel no. \n");
    fprintf(stderr, "      -h            : This usage print\n");
    fprintf(stderr, "      -?            : This usage print\n");
    fprintf(stderr, "\n");
 
    return ;
}

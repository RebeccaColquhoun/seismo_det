#include <s4win2sac.h>
#include    <stdio.h>
#include <stdlib.h>
#include    <string.h>
/* #define MAXBYTE 500000 */
extern int giKwin32;
int 
read_data(unsigned char **ptr, FILE * fp)
{
    static unsigned int size;
/*     int     re; */
    unsigned int re;
    int     rsize;
    int     iRet;
    int     iCount;
/*     static int ii04 = 4; */
    unsigned char ucDat[16];
    if (giKwin32 == 0) {
        iCount = fread(&re, 1, 4, fp);
        if (iCount != 4) {
            iRet = 0;
            goto ret;
        }
    } else {
        iCount = fread(ucDat, 1, 16, fp);
        if (iCount != 16) {
            iRet = 0;
            goto ret;
        }
        memmove(&re, &ucDat[12], 4);
    }
/*   printf("----------- re=%d  %08x\n",re, re); */
/*     bytrev_((unsigned char *) &re, &ii04); */
    swap4b((unsigned int *)&re);
/*   printf("----------- re=%d  %08x\n",re, re); */
#if DEBUG
    fprintf(stderr, "BLOCK SIZE = %d bytes\n", re);
    fprintf(stderr, "PTR = %x\n", *ptr);
#endif
    if (*ptr == 0) {
        size = re * 2;
        if (NULL == (*ptr = (unsigned char *) malloc(size+100))) {
/*         if (NULL == (*ptr = (unsigned char *) malloc(size = MAXBYTE))) { */
            perror("malloc ");
            exit(1);
        }
    } else {
        if (re > size) {
/*             printf("***** ERROR ***** The block size was maximum over.(%d %d)(%s %d)\n", */
/*                        MAXBYTE, re, __FILE__, __LINE__); */
/*             exit (0); */
            size = re * 2;
            if (NULL == (*ptr = (unsigned char *) realloc(*ptr, size+100))) {
                perror("realloc ");
                exit(1);
            }
        }
    }
    if (giKwin32 == 0) {
        *(int *) *ptr = re;
        rsize = fread(*ptr + 4, 1, (size_t) (re - 4), fp);
        if (rsize != re - 4) {
            iRet = 0;
            goto ret;
        }
    } else {
        *(int *) *ptr = re + 16;
        memmove(*ptr + 4, ucDat, 16);
        rsize = fread(*ptr + 20, 1, (size_t) (re), fp);
        if (rsize != re) {
            iRet = 0;
            goto ret;
        }
    }
    iRet = re;
ret:;
    return iRet;
}

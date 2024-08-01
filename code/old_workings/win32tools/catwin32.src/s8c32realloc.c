#include <stdio.h>
#include <stdlib.h>
#include <s8c32_type.h>
#include <s8c32_prot.h>
void c32realloc(
    C32_HEADER **pptHeader,    /** (I/O) ヘッダーのポインター **/
    int          iNheader      /** ( I ) 確保するヘッダーの個数 **/
)
{
    if (*pptHeader == NULL) { /* 新規に確保 */
        *pptHeader = (C32_HEADER *)malloc(sizeof(C32_HEADER)*iNheader);
        if (*pptHeader == NULL) {
            fprintf(stderr, "***** ERROR ***** %d byte memory alloc error.(c32realloc)\n",
                                           (int)sizeof(C32_HEADER)*iNheader);
            exit (0);
        }
    } else {                  /* 再確保 */
        *pptHeader = (C32_HEADER *)realloc(*pptHeader, sizeof(C32_HEADER)*iNheader);
        if (*pptHeader == NULL) {
            fprintf(stderr, "***** ERROR ***** %d byte memory alloc error.(c32realloc)\n", 
                                           (int)sizeof(C32_HEADER)*iNheader);
            exit (0);
        }
    }
}

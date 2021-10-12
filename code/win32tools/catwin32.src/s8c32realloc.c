#include <stdio.h>
#include <stdlib.h>
#include <s8c32_type.h>
#include <s8c32_prot.h>
void c32realloc(
    C32_HEADER **pptHeader,    /** (I/O) �إå����Υݥ��󥿡� **/
    int          iNheader      /** ( I ) ���ݤ���إå����θĿ� **/
)
{
    if (*pptHeader == NULL) { /* �����˳��� */
        *pptHeader = (C32_HEADER *)malloc(sizeof(C32_HEADER)*iNheader);
        if (*pptHeader == NULL) {
            fprintf(stderr, "***** ERROR ***** %d byte memory alloc error.(c32realloc)\n",
                                           (int)sizeof(C32_HEADER)*iNheader);
            exit (0);
        }
    } else {                  /* �Ƴ��� */
        *pptHeader = (C32_HEADER *)realloc(*pptHeader, sizeof(C32_HEADER)*iNheader);
        if (*pptHeader == NULL) {
            fprintf(stderr, "***** ERROR ***** %d byte memory alloc error.(c32realloc)\n", 
                                           (int)sizeof(C32_HEADER)*iNheader);
            exit (0);
        }
    }
}

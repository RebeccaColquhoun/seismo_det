#include <stdlib.h>
#include <s8c32_type.h>
#include <s8c32_prot.h>
int maxalloc(
    void **ppvPtr,    /** (I/O) �ݥ��� **/
    int   iAllbyte,   /** ( I ) alloc����Х��ȿ� **/
    int  *piMaxbyte   /** ( I ) ���ߤΥХ��ȿ� **/ 
)
{
    int iRet;
    iRet = 1;
    if (*ppvPtr == NULL) {
        *ppvPtr = malloc((size_t)iAllbyte);
        if (*ppvPtr == NULL) goto ret;
        *piMaxbyte = iAllbyte;  
    } else if (*piMaxbyte < iAllbyte) {
        *ppvPtr = realloc(*ppvPtr, (size_t)iAllbyte);
        if (*ppvPtr == NULL) goto ret;
        *piMaxbyte = iAllbyte;
    }
    iRet = 0;
ret:;
    return iRet;
}

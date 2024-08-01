#include <s8c32_type.h>
#include <s8c32_prot.h>
int c32cmp1(
    C32_HEADER * pstData1,
    C32_HEADER * pstData2
)
{
    int iRet;
    int ia;
    iRet = 0;
    for (ia=0; ia<8; ia++) {
        if (pstData1->ucStart[ia] < pstData2->ucStart[ia]) {
            iRet = -1;
            break;
        } else if (pstData1->ucStart[ia] > pstData2->ucStart[ia]) {
            iRet = 1;
            break;
        }
    }
#if 0
    if (iRet == 0) {
        if (pstData1->tOffset < pstData2->tOffset) {
            iRet = -1;
        } else if (pstData1->tOffset > pstData2->tOffset) {
            iRet = 1;
        }
    }
#else
    if (iRet == 0) {
        if (pstData1->uhChanno0 < pstData2->uhChanno0) {
            iRet = -1;
        } else if (pstData1->uhChanno0 > pstData2->uhChanno0) {
            iRet = 1;
        } else {
            if (pstData1->uhChanno < pstData2->uhChanno) {
                iRet = -1;
            } else if (pstData1->uhChanno > pstData2->uhChanno) {
                iRet = 1;
            }
        }
    }
#endif
    return(iRet);
}  /** end of c32cmp1 **/

#include <s8c32_type.h>
#include <s8c32_prot.h>
int c32cmp2(
    WIDECHAN * pstData1,
    WIDECHAN * pstData2
)
{
    int iRet;
    iRet = 0;
    if (pstData1->uhChan0 < pstData2->uhChan0) {
        iRet = -1;
    } else if (pstData1->uhChan0 > pstData2->uhChan0) {
        iRet = 1;
    } else {
        if (pstData1->uhChan < pstData2->uhChan) {
            iRet = -1;
        } else if (pstData1->uhChan > pstData2->uhChan) {
            iRet = 1;
        }
    }
    return(iRet);
}  /** end of c32cmp2 **/

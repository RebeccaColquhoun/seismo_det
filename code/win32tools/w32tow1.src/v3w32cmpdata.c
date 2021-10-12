#include <v3win32_type.h>
#include <v3win32_prot.h>
int
w32cmpdata(
    WIN32_DATA * pstData1,
    WIN32_DATA * pstData2
)
{
    int ia;
    int iRet;
    iRet = 0;
    for(ia=0; ia<8; ia++) {
        if (pstData1->iDate[ia] < pstData2->iDate[ia]) {
            iRet = -1;
            break;
        } else if (pstData1->iDate[ia] > pstData2->iDate[ia]) {
            iRet = 1;
            break;
        }
    }
    if (iRet == 0) {
        if (pstData1->uhChanno < pstData2->uhChanno) {
            iRet = -1;
        } else if (pstData1->uhChanno > pstData2->uhChanno) {
            iRet = 1;
        } else {
            if (pstData1->iSeq < pstData2->iSeq) {
                iRet = -1;
            } else if (pstData1->iSeq > pstData2->iSeq) {
                iRet = 1;
            }
        }
    }
    return(iRet);
}

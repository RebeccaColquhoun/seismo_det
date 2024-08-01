#include <stdio.h>
#include <stdlib.h>
#include <y2wchch_prot.h>
/* #include <y0wadd_n_man.h> */
extern int     giKbegin;
extern int     giKwin32;
extern int     giKwrite;
/** WIN32の時、先頭のフォーマット部を書いていない場合は書く **/
int form_write(FILE * f_out)
{
    static int iForm = 0;
    size_t iSize;
    int iRet;
    iRet = 0;
    if (giKwin32 == 1) {
        if (giKwrite == 0) {
            giKwrite = 1;
            iSize = fwrite(&iForm, 1, 4, f_out);
            if (iSize != 4) {
                iRet = 1;
            }
        }
    }
    return iRet;
}

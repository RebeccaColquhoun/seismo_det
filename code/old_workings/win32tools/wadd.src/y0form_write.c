#include <y0wadd_n_man.h>
extern int giKbegin_main;
extern int giKbegin_sub;
extern int giKwin32_main;
extern int giKwin32_sub;
extern int giKwin32_both;
extern int giKwrite;
/** WIN32の時、先頭のフォーマット部を書いていない場合は書く **/
int form_write(FILE * f_out)
{
    static int iForm = 0;
    size_t iSize;
    int iRet;
    iRet = 0;
    if (giKwin32_both) {
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

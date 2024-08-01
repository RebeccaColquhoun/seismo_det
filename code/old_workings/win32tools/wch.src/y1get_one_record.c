#include <string.h>
#include <y1wch_n_man.h>
#include <y1wch_prot.h>
#include <stdlib.h>
extern int     giKbegin;
extern int     giKwin32;
extern int     giKwrite;
void get_one_record()
{
    int     iKer;
    int     re;
    int     new_size;
    int     iComp;
    iComp = 0;
    while (read_data() > 0) {
    	if (iComp == 0){		/** 出力判断値(win1[10]/win32[16])の設定 **/
			if (giKwin32 == 0){
				 iComp = 10;
			} else {
				iComp = 16;
			}
		}
        /* read one sec */
        if ((new_size = select_ch(ch_table, buf, outbuf)) > iComp) {
            /* write one sec */
            if (giKwin32 == 0) {
                if ((re = fwrite(outbuf, 1, mkint(outbuf), stdout)) == 0) {
                    exit(1);
                }
            } else {
                iKer = form_write(stdout);
                if (iKer) {
                    exit (1);
                }
                new_size -= 16;
                new_size = mkint((unsigned char *)&new_size);  /** 正数でない **/
                memmove(outbuf+16, &new_size, 4);
                re = mkint(outbuf);
                if ((fwrite(outbuf+4, 1, re, stdout)) != re) {
                    exit(1);
                }
            }
        }
    }
}

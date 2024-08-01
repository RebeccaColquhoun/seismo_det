#include <y2wchch_man.h>
#include <y2wchch_prot.h>
#include <stdlib.h>
extern int     giKbegin;
extern int     giKwin32;
extern int     giKwrite;
void get_one_record()
{
    int     iKer;
    int     new_size;
    int     re;
    while (read_data() > 0) {
        /* read one sec */
        if ((new_size = select_ch(ch_table0, ch_table1, buf, outbuf)) > 10) {
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
#if 0
                new_size -= 16;
                new_size = mkint(&new_size);  /** 正数でない **/
                memmove(outbuf+16, &new_size, 4);
#endif
                re = mkint(outbuf);
                if ((fwrite(outbuf+4, 1, re, stdout)) != re) {
                    exit(1);
                }
            }
        }
#if DEBUG1
        fprintf(stderr, "in:%d B out:%d B\n", mkint(buf), mkint(outbuf));
#endif
    }
#if DEBUG1
    fprintf(stderr, " : done\n");
#endif
}

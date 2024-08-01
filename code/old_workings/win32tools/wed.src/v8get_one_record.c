#include <v8winlib.h>
#include <v8wed_ext.h>
#include <stdlib.h>
extern int     giKbegin;
extern int     giKwin32;
extern int     giKwrite;
extern int     giKnohead;
void get_one_record()
{
    int     i;
    int     ia;
    int     iii;
    int     iSize;
    int     iComp;
    unsigned int outsize;
    iComp = 6;
    if (giKwin32 == 1) iComp = 8;
    for (i = 0; i < 6; i++) {
        dec_end[i] = dec_start[i];
    }
#if 0
    for (i = leng - 1; i > 0; i--) {
        dec_end[5]++;
        adj_time(dec_end);
    }
#else
    dec_end[5] += leng-1;
    adj_time2(dec_end);
#endif
    /* read first block */
    do {
        if (read_data() <= 0) {
            exit(1);
        }
        if (giKwin32 == 0) {
            bcd_dec(dec_now, (char *) buf + 4);
        } else {
            bcd_dec8(dec_now, (char *) buf + 4);
        }
    } while (time_cmp(dec_start, dec_now, 6) > 0);
    while (1) {
        outsize = select_ch(guiSysch, nch, buf, outbuf);
        if (giKwin32 == 0) {
            if (outsize > 10 || leng >= 0) {
                /* write one sec */
                if (fwrite(outbuf, 1, outsize, stdout) == 0) {
                    exit(1);
                }
            }
        } else {
            if (outsize > 20 || leng >= 0) {
                if (giKwrite == 0) {  /** フォーマットＩＤ等出力 **/
                    giKwrite = 1;
                    iii = 0;
                    if (giKnohead == 0) {  /** **/
                        iSize = fwrite(&iii, 1, 4, stdout);
                        if (iSize != 4) {
                            fprintf(stderr,"***** write error !!!!! *****\n");
                            exit(1);
                        }
                    }
                }
                /* write one sec */
                for (ia=0; ia<28; ia++) {
                }
                if (fwrite(outbuf+4, 1, outsize, stdout) == 0) {
                    fprintf(stderr,"***** write error !!!!! *****\n");
                    exit(1);
                }
            }
        }
        if (leng >= 0 && time_cmp(dec_now, dec_end, 6) == 0) {
            break;
        }
        /* read one sec */
        if (read_data() <= 0) {
            break;
        }
        if (giKwin32 == 0) {
            bcd_dec(dec_now, (char *) buf + 4);
        } else {
            bcd_dec8(dec_now, (char *) buf + 4);
        }
        if (leng >= 0 && time_cmp(dec_now, dec_end, 6) > 0) {
            break;
        }
    }
}

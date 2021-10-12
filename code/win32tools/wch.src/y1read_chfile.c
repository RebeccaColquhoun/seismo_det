#include <stdlib.h>
#include <y1wch_n_man.h>
#include <y1wch_prot.h>
int read_chfile(char   * chfile)
{
    FILE   *fp;
    int     i, j;
    unsigned int k;
    char    tbuf[1024];
    if ((fp = fopen(chfile, "rt")) != NULL) {
        if (giKbigchno == -1) {
            for (i = 0; i < 65536; i++) {
                ch_table[i] = 0;
            }
        } else {
            for (i = 0; i < MAX_CH_TABLE_W; i++) {
                ulCh_table_w[i] = (unsigned int)0xffffffff;
            }
        }
        i = j = 0;
        iNch_table_w = 0;
        while (fgets(tbuf, 1024, fp)) {
            if (*tbuf == '#' || sscanf(tbuf, "%x", &k) < 0) continue;
            if (giKbigchno == -1) {
                k &= 0xffff;
                if (ch_table[k] == 0) {
                    ch_table[k] = 1;
                    j++;
                }
                i++;
            } else {
                if (iNch_table_w >= MAX_CH_TABLE_W) {
                    fprintf(stderr, "***** ERROR ***** The number of channel is max. over.(%d)\n", MAX_CH_TABLE_W);
                    exit (0);
                }
                ulCh_table_w[iNch_table_w] = k;
                iNch_table_w++;
                j = iNch_table_w;
            }
        }
    } else {
        fprintf(stderr, "ch_file '%s' not open\n", chfile);
        return 0;
    }
    return j;
}

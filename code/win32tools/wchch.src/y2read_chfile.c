#include <y2wchch_man.h>
#include <y2wchch_prot.h>
int read_chfile(char * chfile)
{
    FILE   *fp;
/*     int     i, j, k; */
    unsigned int uiCh0;
    unsigned int uiCh1;
    char    tbuf[1024];
    giNch = 0;
    if ((fp = fopen(chfile, "r")) != NULL) {
#if DEBUG
        fprintf(stderr, "ch_file=%s\n", chfile);
#endif
/*         for (i = 0; i < 65536; i++) { */
/*             ch_table[i] = i; */
/*         } */
        giNch = 0;
        while (fgets(tbuf, 1024, fp)) {
            if (*tbuf == '#' || sscanf(tbuf, "%x%x", &uiCh0, &uiCh1) < 2) continue;
            
#if DEBUG
            fprintf(stderr, " %08X->%08X", k, j);
#endif
            if (uiCh0 != uiCh1) {
                ch_table0[giNch] = uiCh0;
                ch_table1[giNch] = uiCh1;
                giNch++;
            }
        }
#if DEBUG
        fprintf(stderr, "\n");
#endif
    } else {
        fprintf(stderr, "ch_file '%s' not open\n", chfile);
        return 0;
    }
    return 1;
}

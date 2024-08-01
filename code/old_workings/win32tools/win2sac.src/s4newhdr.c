#include <string.h>
#include <s4win2sac.h>
#define  TRUE 1
#define ITIME 1
#define  FALSE 0
#define NVHDR 6
extern _sac_hdr2 sac_hdr2;
extern _sac_header sac_header;
extern unsigned char    gcOrganize2;
void 
newhdr()
{
    int     i;
    memset(&sac_hdr2, (int)0, sizeof(sac_hdr2));
    memset(&sac_header, (int)0, sizeof(sac_header));
    for (i = 0; i < 70; i++) {
        sac_hdr2.rvar[i] = -12345.0;
    }
    for (i = 0; i < 35; i++) {
        sac_hdr2.ivar[i] = -12345;
    }
/*    for (i = 0; i < 70; i++) { 06/01/11 kjmatsu bug } */
    for (i = 0; i < 5; i++) {
        sac_hdr2.lvar[i] = FALSE;
    }
    for (i = 0; i < 24; i++) {
        strncpy(sac_hdr2.cvar[i], "-12345  ", 8);
    }
    memcpy(&sac_header, &sac_hdr2, sizeof(sac_header));
    sac_header.nvhdr = NVHDR;
    sac_header.iftype = ITIME;
    sac_header.leven = TRUE;
    sac_header.lovrok = TRUE;
    sac_header.lcalda = TRUE;
}

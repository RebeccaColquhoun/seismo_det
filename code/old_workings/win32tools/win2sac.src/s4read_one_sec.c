#include <s4win2sac.h>
#include <string.h>
extern unsigned char    gcOrganize1;
extern unsigned char    gcOrganize2;
extern int giKwin32;
extern int giKwidechan;
extern int winget_smpl( unsigned char *pucPtr, int iOffsize, int iNsampno, int *piAbuf);
int 
read_one_sec(unsigned char *ptr, unsigned int sys_ch, int *abuf)
{
    int     b_size, g_size;
    int     s_rate;
    unsigned char *dp, *pts;
/*     unsigned int gh; */
    unsigned int gh;
    unsigned char *ddp;
    int     iRet;
    int     iKer;
    unsigned int    chid;
    unsigned int bsl;
/*     static int i04 = 4; */
    if (giKwin32 == 0) {
        dp = ptr + 10;
        ddp = ptr + mkint(ptr);
    } else {
        dp = ptr + 20;
        ddp = ptr + mkint(ptr) + 4;
    }
    while (1) {
/* get chl. ID */
        if (giKwin32 == 1) {
            gcOrganize1 = *dp;
            gcOrganize2 = *(dp+1);
            dp += 2;
        }
        if (giKwidechan == 0) {
            pts = (unsigned char *) &chid;
            ptr = dp;
            *pts++ = (*dp++);
            *pts = (*dp++);
        } else {
            pts = (unsigned char *) &chid;
            ptr = dp;
            *pts = *(dp-2);
            pts++;
            *pts = *(dp-1);
            pts++;
            *pts = *(dp);
            pts++;
            *pts = *(dp+1);
            dp += 2;
        }
        swap4b((unsigned int *)&chid);
        if (giKwidechan == 0) {
            chid = (chid >> 16) & 0x0000ffff;
        }
#if DEBUG
        fprintf(stderr, "chid = %x (dp=%x)\n", chid, dp);
#endif
/* get sample size indicator */
/*         bsl = 0; */
        pts = (unsigned char *) &bsl;
        *pts = (*dp++);
        bsl = *pts << 24;
        bsl = (((unsigned int)bsl) >> 28) & 0x0000000f;
#if DEBUG
        fprintf(stderr, "bsl = %x, bsl&0x8 = %x (dp=%x)\n", bsl, bsl & 0x8, dp);
#endif
        if ((int) (bsl & 0x8) == 0) {   /* OLD format */
            pts = (unsigned char *) &gh;
            dp--;
            *pts++ = (*dp++);
            *pts = (*dp++);
/*             bytrev_((unsigned char *) &gh, &i04); */
            swap4b((unsigned int *)&gh);
            s_rate = ((gh >> 16) & 0x00000fff);
            b_size = (gh >> 28) & 0x0000000f;
#if DEBUG
            fprintf(stderr, "OLD gh = %x, srate = %ld, b_size = %x\n",
                gh, s_rate, b_size);
#endif
        } else {                        /* EXPANDED format */
            pts = (unsigned char *) &gh;
            dp--;
            *pts++ = (*dp++);
            *pts++ = (*dp++);
            *pts = (*dp++);
            s_rate = (gh >> 8) & 0x000fffff;
            b_size = (gh >> 28) & 0x7;
#if DEBUG
            fprintf(stderr, "NEW gh = %x, srate = %ld, b_size = %x\n",
                gh, s_rate, b_size);
#endif
        }
        if (s_rate > 2000) {
            fprintf(stderr, "***** ERROR ***** The sampling number is maximum over.(2000)\n");
            exit(0);
        }
        if ((int) b_size != 0) {
            g_size = b_size * (s_rate - 1) + 4;
        } else {
            g_size = (s_rate >> 1) + 4;
        }
        if (chid == sys_ch) {
            break;
        } else {
            if ((dp += g_size) >= ddp) {
                iRet = 0;
                goto ret;
            }
        }
    }
#if 0
    /* read group */
    pts = (unsigned char *) &abuf[0];
    *pts++ = (*dp++);
    *pts++ = (*dp++);
    *pts++ = (*dp++);
    *pts = (*dp++);
    if (s_rate == 1) {
        iRet = s_rate;
        goto ret;
    }
    switch (b_size) {
    case 0:
        for (i = 1; i < s_rate; i += 2) {
            abuf[i] = abuf[i - 1] + ((*(char *) dp) >> 4);
            if (i+1 < s_rate) {
                abuf[i + 1] = abuf[i] + (((char) (*(dp++) << 4)) >> 4);
            }
        }
        break;
    case 1:
        for (i = 1; i < s_rate; i++)
            abuf[i] = abuf[i - 1] + (*(char *) (dp++));
        break;
    case 2:
        for (i = 1; i < s_rate; i++) {
            pts = (unsigned char *) &shreg;
            *pts++ = (*dp++);
            *pts = (*dp++);
            abuf[i] = abuf[i - 1] + shreg;
        }
        break;
    case 3:
        for (i = 1; i < s_rate; i++) {
            pts = (unsigned char *) &inreg;
            *pts++ = (*dp++);
            *pts++ = (*dp++);
            *pts = (*dp++);
            abuf[i] = abuf[i - 1] + (inreg >> 8);
        }
        break;
    case 4:
        for (i = 1; i < s_rate; i++) {
            pts = (unsigned char *) &inreg;
            *pts++ = (*dp++);
            *pts++ = (*dp++);
            *pts++ = (*dp++);
            *pts = (*dp++);
            abuf[i] = abuf[i - 1] + inreg;
        }
        break;
    default:
        iRet = 0;
        goto ret;
    }
#else
    iKer = winget_smpl(ptr, b_size, s_rate, (int *) abuf);
    if (iKer) {
        iRet = 0;
        goto ret;
    }
#endif
    iRet = s_rate;
ret:;
    return iRet;                        /* normal return */
}

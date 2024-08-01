#include <string.h>
#include <v9dewin_ext.h>
extern int giKbegin;
extern int giKwin32;
extern int giKwidechan;
int read_one_sec(
    unsigned char *ptr,                /* input */
    unsigned int uiSysch,              /* uiSysch = sys*256 + ch */
    int *abuf                          /* output */
)
{
    unsigned short uhCh0;
    int iRet;
    int     b_size, g_size;
    register int i, s_rate;
    register unsigned char *dp, *pts;
    unsigned int ulgh;
    unsigned char gh[5];
    unsigned char *ddp;
    short   shreg;
    int     inreg;
    int iii;
    unsigned int uiWork;
    if (giKwin32 == 0) {
        dp = ptr + 10;
        memmove(&iii, ptr, 4);
        ddp = ptr + iii;            /* Don't SWAPL */
    } else {
        dp = ptr + 20;    /** チャンネルブロックの先頭 **/
        memmove(&iii, ptr, 4);
        ddp = ptr + iii + 4;
    }
    while (1) {
        if (giKwin32 != 0) dp += 2;
        if (giKwidechan == 1) {
            memmove(&uhCh0, dp-2, 2);
            swap2b((unsigned short *)&uhCh0);
        }
        gh[0] = dp[0];
        gh[1] = dp[1];
        gh[2] = dp[2];
        gh[3] = dp[3];
        memmove(&ulgh, gh, 4);
        /* channel header = 4 byte */
        if ((gh[2] & 0x80) == 0x0) {
            s_rate = gh[3] + (((int) (gh[2] & 0x0f)) << 8);
            b_size = ((gh[2] >> 4) & 0x7);
            if (b_size) {
                g_size = b_size * (s_rate - 1) + 8;
            } else {
                g_size = (s_rate >> 1) + 8;
            }
            uiWork = (unsigned int)(gh[1] + (((int) gh[0]) << 8));
            if (giKwidechan == 1) {
                uiWork = (uhCh0 << 16) | uiWork;
            }
            if (uiWork == uiSysch) {
                /* advance pointer and break */
                dp += 4;
                break;
            } else if ((dp += g_size) >= ddp) {
                iRet = 0;
                goto ret;
            }
        } else {
            /* channel header = 5 byte */
            gh[4] = dp[4];
            s_rate = gh[4] + (((int) gh[3]) << 8) + (((int) (gh[2] & 0x0f)) << 16);
            b_size = ((gh[2] >> 4) & 0x7);
            if (b_size) {
                g_size = b_size * (s_rate - 1) + 9;
            } else {
                g_size = (s_rate >> 1) + 9;
            }
            if ((gh[1] + (((int) gh[0]) << 8)) == uiSysch) {
                /* advance pointer and break */
                dp += 5;
                break;
            } else if ((dp += g_size) >= ddp) {
                iRet = 0;
                goto ret;
            }
        }
    }
    /* read group */
    pts = (unsigned char *) &abuf[0];
    *pts++ = (*dp++);
    *pts++ = (*dp++);
    *pts++ = (*dp++);
    *pts = (*dp++);
    swap4b((unsigned int *)&abuf[0]);
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
        for (i = 1; i < s_rate; i++) {
            abuf[i] = abuf[i - 1] + (*(char *) (dp++));
        }
        break;
    case 2:
        for (i = 1; i < s_rate; i++) {
            pts = (unsigned char *) &shreg;
            *pts++ = (*dp++);
            *pts = (*dp++);
            swap2b((unsigned short *)&shreg);
            abuf[i] = abuf[i - 1] + shreg;
        }
        break;
    case 3:
        for (i = 1; i < s_rate; i++) {
            pts = (unsigned char *) &inreg;
            *pts++ = (*dp++);
            *pts++ = (*dp++);
            *pts = (*dp++);
            swap4b((unsigned int *)&inreg);
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
            swap4b((unsigned int *)&inreg);
            abuf[i] = abuf[i - 1] + inreg;
        }
        break;
    default:
        iRet = 0;
        goto ret;
    }
    iRet = s_rate;                    /* normal return */
ret:;
    return iRet;
}

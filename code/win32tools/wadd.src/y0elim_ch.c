#include <y0wadd_n_man.h>
extern int giKbegin_main;
extern int giKbegin_sub;
extern int giKwin32_main;
extern int giKwin32_sub;
extern int giKwin32_both;
extern int giKwrite;
extern int giKwidechan;
int elim_ch(unsigned int *sys_ch, int n_ch, unsigned char *old_buf, unsigned char *new_buf)
{
    int     iii;
    int     i, j, size, gsize, new_size, sr;
    unsigned char *ptr, *new_ptr, *ptr_lim;
    unsigned int gh;
    unsigned short int uhCh0;
    unsigned short int uhCh;
    unsigned int uiChm = 0;
#if 0  /** { **/ 
    memmove(&size, old_buf, 4);
    swap4b((unsigned int *)&size);
    if (giKwin32_both) {
        ptr_lim = old_buf + size + 4;
    } else {
        ptr_lim = old_buf + size;
    }
#else  /** } else {**/ 
    if (giKwin32_both) {
        memmove(&size, old_buf+16, 4);
        swap4b((unsigned int *)&size);
        ptr_lim = old_buf + size + 20;
    } else {
        memmove(&size, old_buf, 4);
        swap4b((unsigned int *)&size);
        ptr_lim = old_buf + size;
    }
#endif  /** } **/ 
    if (giKwin32_both) {
        ptr = old_buf + 4;
        new_ptr = new_buf + 4;
        for (i = 0; i < 16; i++) {
            *new_ptr = (*ptr);
            new_ptr++;
            ptr++;
        }
        new_size = 16;
    } else {
        ptr = old_buf + 4;
        new_ptr = new_buf + 4;
        for (i = 0; i < 6; i++) {
            *new_ptr++ = (*ptr++);
        }
        new_size = 10;
    }
    do {
        if (giKwin32_both) ptr += 2;
        if (giKwidechan == 1) {
            memmove(&uhCh0, ptr-2, 2);
            swap2b((unsigned short int *)&uhCh0);
        }
        memmove(&gh, ptr, 4);
        swap4b((unsigned int *)&gh);
        if (giKwidechan == 1) {
            memmove(&uhCh, ptr, 2);
            swap2b((unsigned short int *)&uhCh);
            uiChm = uhCh0 << 16;
            uiChm = uiChm | uhCh;
        }
        i = gh >> 16;
        sr = gh & 0xfff;
        if ((gh >> 12) & 0xf) {
            gsize = ((gh >> 12) & 0xf) * (sr - 1) + 8;
        } else {
            gsize = (sr >> 1) + 8;
        }
        for (j = 0; j < n_ch; j++) {
            if (giKwidechan == 1) {
                if (uiChm == sys_ch[j]) {
                    break;
                }
            } else {
                if ((unsigned int)i == sys_ch[j]) {
                    break;
                }
            }
        }
        if (n_ch == 0 || j == n_ch) {
            if (giKwin32_both) {
                gsize += 2;
                new_size += gsize;
                ptr -= 2;
            } else {
                new_size += gsize;
            }
            while (gsize-- > 0) {
                *new_ptr = (*ptr);
                new_ptr++;
                ptr++;
            }
        } else {
            ptr += gsize;
        }
    } while (ptr < ptr_lim);
    memmove(new_buf, &new_size, 4);
    swap4b((unsigned int *)new_buf);
    memmove(&iii, new_buf, 4);
    swap4b((unsigned int *)&iii);
    for (iii=0; iii<8; iii++) {
    }
    return new_size;
}

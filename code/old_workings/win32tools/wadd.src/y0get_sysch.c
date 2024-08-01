#include <y0wadd_n_man.h>
extern int giKbegin_main;
extern int giKbegin_sub;
extern int giKwin32_main;
extern int giKwin32_sub;
extern int giKwin32_both;
extern int giKwrite;
extern int giKwidechan;
int get_sysch(unsigned char *buf, unsigned int *sys_ch)
{
    int     i, size, gsize, sr;
    unsigned char *ptr, *ptr_lim;
    unsigned int gh;
    unsigned short int uhCh0;
#if 0  /** { **/ 
    memmove(&size, buf, 4);
    swap4b((unsigned int *)&size);
    if (giKwin32_both) {
        ptr_lim = buf + size + 4;
        ptr = buf + 20;
    } else {
        ptr_lim = buf + size;
        ptr = buf + 10;
    }
#else  /** } else {**/ 
    if (giKwin32_both) {
        memmove(&size, buf+16, 4);
        swap4b((unsigned int *)&size);
        ptr_lim = buf + size + 20;
        ptr = buf + 20;
    } else {
        memmove(&size, buf, 4);
        swap4b((unsigned int *)&size);
        ptr_lim = buf + size;
        ptr = buf + 10;
    }
#endif  /** } **/ 
    i = 0;
    do {
        if (giKwin32_both) ptr += 2;
        if (giKwidechan == 1) {
            memmove(&uhCh0, ptr-2, 2);
            swap2b((unsigned short int *)&uhCh0);
        }
        memmove(&gh, ptr, 4); 
        swap4b((unsigned int *)&gh);
        if (giKwidechan == 0) {
            sys_ch[i] = gh >> 16;
        } else {
            sys_ch[i] = uhCh0 << 16;
            sys_ch[i] = sys_ch[i] | (gh >> 16);
        }
        i++;
        sr = gh & 0xfff;
        if ((gh >> 12) & 0xf) {
            gsize = ((gh >> 12) & 0xf) * (sr - 1) + 8;
        } else {
            gsize = (sr >> 1) + 8;
        }
#if DEBUG
        printf("gh=%08x sr=%d gs=%d\n", gh, sr, gsize);
#endif
        ptr += gsize;
    } while (ptr < ptr_lim);
    return i;
}

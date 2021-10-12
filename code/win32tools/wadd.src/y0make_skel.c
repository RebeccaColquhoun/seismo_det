#include <y0wadd_n_man.h>
extern int giKbegin_main;
extern int giKbegin_sub;
extern int giKwin32_main;
extern int giKwin32_sub;
extern int giKwin32_both;
extern int giKwrite;
void make_skel(unsigned char *old_buf, unsigned char *new_buf)
{
    int     i, size, gsize, new_size, sr;
    unsigned char *ptr, *new_ptr, *ptr_lim;
    unsigned int gh;
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
    ptr = old_buf + 4;
    new_ptr = new_buf + 4;
    if (giKwin32_both) {
        for (i = 0; i < 16; i++) {
            *new_ptr++ = (*ptr++);
        }
        new_size = 16;
    } else {
        for (i = 0; i < 6; i++) {
            *new_ptr++ = (*ptr++);
        }
        new_size = 10;
    }
    do {
        if (giKwin32_both) {
            *new_ptr++ = (*ptr++);
            *new_ptr++ = (*ptr++);
        }
        memmove(&gh, ptr, 4);
        swap4b((unsigned int *)&gh);
        i = gh >> 16;
        sr = gh & 0xfff;
        if ((gh >> 12) & 0xf) {
            gsize = ((gh >> 12) & 0xf) * (sr - 1) + 8;
        } else {
            gsize = (sr >> 1) + 8;
        }
        ptr += gsize;
        gh &= 0xffff0fff;
        gsize = (sr >> 1) + 8;
        memmove(new_ptr, &gh, 4);
        swap4b((unsigned int *)new_ptr);
        new_ptr += 4;
        for (i = 0; i < gsize - 4; i++) {
            *new_ptr++ = 0;
        }
        if (giKwin32_both) gsize += 2;
        new_size += gsize;
    } while (ptr < ptr_lim);
    memmove(new_buf, &new_size, 4);
    swap4b((unsigned int *)new_buf);
}

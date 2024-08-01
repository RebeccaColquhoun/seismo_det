#include <string.h>
#include <y1wch_n_man.h>
#include <y1wch_prot.h>
extern int     giKbegin;
extern int     giKwin32;
extern int     giKwrite;
int select_ch(unsigned char *table, unsigned char *old_buf, unsigned char *new_buf)
{
    int kkk;
    int ia;
    int     iComp;
    int     i, size, gsize, new_size, sr;
    unsigned int lCh = 0;
    unsigned char *ptr, *new_ptr, *ptr_lim;
    unsigned int gh;
    unsigned int * w_ptr;
    iComp = 6;
    if (giKwin32 == 1) iComp = 16;
    size = mkint(old_buf);
    if (giKwin32 == 0) {
        ptr_lim = old_buf + size;
    } else {
        ptr_lim = old_buf + size + 4;
    }
    ptr = old_buf + 4;
    new_ptr = new_buf + 4;
    w_ptr = (unsigned int *)new_ptr;
    for (i = 0; i < iComp; i++) {
        *new_ptr++ = (*ptr++);
    }
    if (giKwin32 == 0) {
        new_size = 10;
    } else {
        new_size = 16;
    }
    do {
        if (giKwin32 == 1) {
            if (giKbigchno != -1) {
                lCh = mkint(ptr);
                mkint(ptr);
            }
            ptr += 2;                    
        }
        gh = mkint(ptr);
        i = gh >> 16;
        sr = gh & 0xfff;
        if ((gh >> 12) & 0xf) {
            gsize = ((gh >> 12) & 0xf) * (sr - 1) + 8;
        } else {
            gsize = (sr >> 1) + 8;
        }
        if (giKbigchno == -1) {
            kkk = table[i];
        } else {
            kkk = 0;
            for (ia=0; ia<iNch_table_w; ia++) {
                if (ulCh_table_w[ia] == lCh) {
                    kkk = 1;
                    break;
                }
            }
        }
        if (kkk) {
            if (giKwin32 == 1) {
                gsize += 2;
                ptr -= 2;
            }
            new_size += gsize;
            while (gsize-- > 0) {
                *new_ptr++ = (*ptr++);
            }
        } else {
            ptr += gsize;
        }
    } while (ptr < ptr_lim);
    ptr = (unsigned char *) &new_size;
    memmove(new_buf, ptr, 4);
    swap4b((unsigned int *)new_buf);
    return new_size;
}

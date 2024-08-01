#include <string.h>
#include <y2wchch_man.h>
#include <y2wchch_prot.h>
extern int     giKbegin;
extern int     giKwin32;
extern int     giKwrite;
extern int     giKwidechan;
int select_ch(unsigned int * table0, unsigned int * table1, unsigned char * old_buf, unsigned char * new_buf)
{
    int ia;
    unsigned int uiChm = 0;
    unsigned int uiChm0 = 0;
    unsigned int uiChm1 = 0;
    unsigned short uhCh0w = 0;
    unsigned short uhChw;
    int     iComp;
    int     i, size, gsize, new_size, sr;
    unsigned char *ptr, *new_ptr, *ptr_lim;
    unsigned int ch0 = 0;
    unsigned int ch;
    unsigned int gh0;
    unsigned int gh;
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
            *new_ptr++ = (*ptr++);
            *new_ptr++ = (*ptr++);
            new_size += 2;
        }
        gh = mkint(ptr);
        ch = gh >> 16;
        if (giKwidechan == 1) {
            gh0 = mkint(ptr-2);
            ch0 = gh0 >> 16;
        }
        sr = gh & 0xfff;
        if ((gh >> 12) & 0xf) {
            gsize = ((gh >> 12) & 0xf) * (sr - 1) + 8;
        } else {
            gsize = (sr >> 1) + 8;
        }
        if (giKwidechan == 1) {
            uhCh0w = ((ch0 >> 16) & 0x0000ffff);
            uhChw = (ch & 0x0000ffff);
            uiChm0 = ch0 << 16;
            uiChm1 = ch & 0x0000ffff;
            uiChm = uiChm0 | uiChm1;
            for (ia=0; ia<giNch; ia++) {
                if (ch_table0[ia] == uiChm) break;
            }
            if (ia < giNch) {
                uhCh0w = ((ch_table1[ia] >> 16) & 0x0000ffff);
                uhChw = (ch_table1[ia] & 0x0000ffff);
                new_ptr -= 2;
                *new_ptr++ = uhCh0w >> 8;
                *new_ptr++ = uhCh0w;
                *new_ptr++ = uhChw >> 8;
                *new_ptr++ = uhChw;
            } else {
                uhCh0w = ch0 & 0x0000ffff;
                uhChw = (ch & 0x0000ffff);
                new_ptr -= 2;
                *new_ptr++ = uhCh0w >> 8;
                *new_ptr++ = uhCh0w;
                *new_ptr++ = uhChw >> 8;
                *new_ptr++ = uhChw;
            }
            ptr += 2;
        } else {
            for (ia=0; ia<giNch; ia++) {
                if (ch_table0[ia] == ch) break;
            }
            if (ia < giNch) {
                uhChw = (ch_table1[ia] & 0x0000ffff);
                *new_ptr++ = uhChw >> 8;
                *new_ptr++ = uhChw;
            } else {
            	*new_ptr++ = (*ptr++);
            	*new_ptr++ = (*ptr++);
            	ptr -= 2;
            }
            ptr += 2;
        }
        new_size += gsize;
        gsize -= 2;
        while (gsize-- > 0) {
            *new_ptr++ = (*ptr++);
        }
    } while (ptr < ptr_lim);
    ptr = (unsigned char *) &new_size;
    memmove(new_buf, ptr, 4);
    swap4b((unsigned int *)new_buf);
    return new_size;
}

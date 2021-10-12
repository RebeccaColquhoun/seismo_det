#include <string.h>
#include <v8wed_ext.h>
extern int giKbegin;
extern int giKwin32;
extern int giKwidechan;
int select_ch(unsigned int *uiSysch, int n_ch, unsigned char *old_buf, unsigned char *new_buf)
{
    int iii;
    int     i, j, size, gsize, new_size, sr;
    unsigned int uiChan0 = 0;
    unsigned int uiChan;
    unsigned char *ptr, *new_ptr, *ptr_lim;
    unsigned char *ptr0 = NULL;
    unsigned char gh[5];
    int iComp;
    iComp = 6;
    if (giKwin32 == 1) iComp = 16;
    size = *((int *)old_buf);
/*     swap4b((unsigned int *)&size); */
/*     size = mkint(old_buf); */
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
            ptr0 = ptr;
            ptr += 2;
        }
        for (i = 0; i < 5; i++) {
            gh[i] = ptr[i];
        }
        if (giKwidechan == 1) {
            uiChan0 = ((((int) ptr0[0]) << 8) + ptr0[1]) & 0x0000ffff;
        }
        uiChan = ((((int) gh[0]) << 8) + gh[1]) & 0x0000ffff;
        /* sampling rate */
        if ((gh[2] & 0x80) == 0x0) {    /* channel header = 4 byte */
            sr = gh[3] + (((int) (gh[2] & 0x0f)) << 8);
        } else {                          /* channel header = 5 byte */
            sr = gh[4] + (((int) gh[3]) << 8) + (((int) (gh[2] & 0x0f)) << 16);
        }
        /* size */
        if ((gh[2] >> 4) & 0x7) {
            gsize = ((gh[2] >> 4) & 0x7) * (sr - 1) + 8;
        } else {
            gsize = (sr >> 1) + 8;
        }
        if (gh[2] & 0x80) {
            gsize++;
        }
        if (giKwidechan == 0) {
            for (j = 0; j < n_ch; j++) {
                if (uiChan == uiSysch[j]) {
                    break;
                }
            }
        } else {
            for (j = 0; j < n_ch; j++) {
                if (uiChan0 == ((uiSysch[j] & 0xffff0000)>>16) &&
                    uiChan == (uiSysch[j] & 0x0000ffff)) {
                    break;
                }
            }
        }
        if (n_ch < 0 || j < n_ch) {
            new_size += gsize;
            if (giKwin32 == 1) {
                new_size += 2;
                ptr -= 2;
                *new_ptr++ = (*ptr++);  /** ÁÈ¿¥¡õÁÈ¿¥ÆâÌÖ£É£Ä **/
                *new_ptr++ = (*ptr++);  /** ÁÈ¿¥¡õÁÈ¿¥ÆâÌÖ£É£Ä **/
            }
            while (gsize-- > 0) {
                *new_ptr++ = (*ptr++);
            }
        } else {
            ptr += gsize;
        }
    } while (ptr < ptr_lim);
    IntToBigEndian(new_size, new_buf);
    if (giKwin32 == 1) {
        iii = new_size - 16;
        IntToBigEndian(iii, &new_buf[16]);
    }
    return new_size;
}

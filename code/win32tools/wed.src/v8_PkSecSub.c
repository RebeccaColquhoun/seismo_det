#include <v8Win2Pack_man.h>
/* 1秒分の win2 データを win に変換 */
WinSize _PkSecSub
        (WinData src, WinSize leng, WinData dst,
    WinNumber(*func) (WinData, WinData))
{
    WinData dst_p = dst, src_p = src, src_end = src + leng;
    WinNumber src_size, dst_size;
    while (src_p < src_end) {
        src_size = WinGetChSize(src_p);
        if (src_size == 0)
            return (dst_p - dst);
        dst_size = func(src_p, dst ? dst_p : NULL);
        src_p += src_size;
        dst_p += dst_size;
    }
    return (dst_p - dst);
}

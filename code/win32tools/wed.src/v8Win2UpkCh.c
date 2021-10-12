#include <v8Win2Pack_man.h>
/* 1チャンネル・1秒分の win2 データを win に変換 */
WinNumber Win2UpkCh
        (WinData src, WinData dst) {
    WinNumber smpl_size, new_size, smpl_rate, data_size;
    WinData dst_p = dst + 8, src_p = src + 8;
    /*
     * サンプリングレート、サンプルサイズの読み込みと新規データサイズの
     * 計算
     */
    GET_SR(src, smpl_size, smpl_rate);
    /*
     * サンプリングレート 1023 Hz 以上の場合は win2 データでないので サ
     * イズは不変
     */
    if (smpl_rate > 1023)
        new_size = smpl_size;
    else
        new_size = smpl_size > 4 ? ((smpl_size + 7) >> 3) << 3 : 4;
    data_size = 8 + ((new_size * (smpl_rate - 1) + 7) >> 3);
    if (dst == NULL)
        return data_size;
    /*
     * チャンネル番号、サンプルサイズ、サンプリングレート、 始めの1サン
     * プルまでコピー
     */
    memcpy(dst, src, 8);
    /*
     * サンプリングレート 1023 Hz 以上の場合は win2 データでないので そ
     * のままコピー
     */
    if (smpl_rate > 1023) {
        memcpy(dst_p, src_p, data_size);
    } else {
        WinNumber k, soffset, doffset, sr_param;
        WinValue value;
        /* サンプルサイズ・サンプリングレートの書き出し */
        sr_param = (new_size >> 3) << 12 | smpl_rate;
        Win_SetValue((WinValue) sr_param, dst + 2, 2);
        /* データ本体の書きだし */
        soffset = doffset = 0;
        /* データサイズが不変の場合、そのままコピー */
        if (new_size == smpl_size) {
            memcpy(dst_p, src_p, data_size);
        } else if ((new_size & 0x07) == 0) {
            new_size >>= 3;
            for (k = 1; k < smpl_rate; k++) {
                value = Win_GetValueB
                    (&src_p[soffset >> 3], soffset & 0x07, smpl_size);
                soffset += smpl_size;
                Win_SetValue(value, &dst_p[doffset], new_size);
                doffset += new_size;
            }
        } else {
            for (k = 1; k < smpl_rate; k++) {
                value = Win_GetValueB
                    (&src_p[soffset >> 3], soffset & 0x07, smpl_size);
                soffset += smpl_size;
                Win_SetValueB(value, &dst_p[doffset >> 3], doffset & 0x07, 4);
                doffset += 4;
            }
            /* 余ったビットを 0 で埋める */
            if (doffset & 0x07)
                dst_p[doffset >> 3] &= 0xf0;
        }
    }
    return data_size;
}

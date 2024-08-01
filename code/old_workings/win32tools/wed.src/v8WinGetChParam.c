#include <v8mkutil_man.h>
#include <v8winlib.h>
ChParam WinGetChParam
        (WinData src) {
    WinData src_p = src;
    WinNumber smpl_size, smpl_rate;
    ChParam ch_param;
    ch_param.blk_ptr = src_p;
    ch_param.ch_number = Win_GetNumber(src_p);
    src_p += 2;
    smpl_size = Win_GetNumber(src_p);
    /* Win format V2 */
    if (smpl_size & 0x8000) {
        smpl_rate = smpl_size & 0x03ff;
        smpl_size = ((smpl_size >> 10) & 0x3f) - 0x1f;
        ch_param.version = 2;
    }
    /* Win format V1 */
    else {
        smpl_rate = smpl_size & 0x0fff;
        smpl_size = (smpl_size >> 12) & 0x0f;
        if (smpl_size > 4) {
            ch_param.ch_number = 0x0000;
            ch_param.smpl_size = 0;
            ch_param.smpl_rate = 0;
            ch_param.blk_size = 0;
            ch_param.version = 0;
            return ch_param;
        }
        smpl_size <<= 3;
        if (smpl_size == 0)
            smpl_size = 4;
        ch_param.version = 1;
    }
    ch_param.smpl_rate = smpl_rate;
    ch_param.smpl_size = smpl_size;
    ch_param.blk_size = 8 + ((smpl_size * (smpl_rate - 1) + 7) >> 3);
    return ch_param;
}

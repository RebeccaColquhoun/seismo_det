#include <v8Win2Pack_man.h>
/* 1�����ͥ롦1��ʬ�� win2 �ǡ����� win ���Ѵ� */
WinNumber Win2UpkCh
        (WinData src, WinData dst) {
    WinNumber smpl_size, new_size, smpl_rate, data_size;
    WinData dst_p = dst + 8, src_p = src + 8;
    /*
     * ����ץ�󥰥졼�ȡ�����ץ륵�������ɤ߹��ߤȿ����ǡ�����������
     * �׻�
     */
    GET_SR(src, smpl_size, smpl_rate);
    /*
     * ����ץ�󥰥졼�� 1023 Hz �ʾ�ξ��� win2 �ǡ����Ǥʤ��Τ� ��
     * ����������
     */
    if (smpl_rate > 1023)
        new_size = smpl_size;
    else
        new_size = smpl_size > 4 ? ((smpl_size + 7) >> 3) << 3 : 4;
    data_size = 8 + ((new_size * (smpl_rate - 1) + 7) >> 3);
    if (dst == NULL)
        return data_size;
    /*
     * �����ͥ��ֹ桢����ץ륵����������ץ�󥰥졼�ȡ� �Ϥ��1����
     * �ץ�ޤǥ��ԡ�
     */
    memcpy(dst, src, 8);
    /*
     * ����ץ�󥰥졼�� 1023 Hz �ʾ�ξ��� win2 �ǡ����Ǥʤ��Τ� ��
     * �Τޤޥ��ԡ�
     */
    if (smpl_rate > 1023) {
        memcpy(dst_p, src_p, data_size);
    } else {
        WinNumber k, soffset, doffset, sr_param;
        WinValue value;
        /* ����ץ륵����������ץ�󥰥졼�Ȥν񤭽Ф� */
        sr_param = (new_size >> 3) << 12 | smpl_rate;
        Win_SetValue((WinValue) sr_param, dst + 2, 2);
        /* �ǡ������Τν񤭤��� */
        soffset = doffset = 0;
        /* �ǡ��������������Ѥξ�硢���Τޤޥ��ԡ� */
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
            /* ;�ä��ӥåȤ� 0 ������ */
            if (doffset & 0x07)
                dst_p[doffset >> 3] &= 0xf0;
        }
    }
    return data_size;
}

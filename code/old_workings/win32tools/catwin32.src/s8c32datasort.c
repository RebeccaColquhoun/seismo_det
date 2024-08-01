#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <s8c32_type.h>
#include <s8c32_prot.h>
void c32datasort(
    C32_HEADER ** pptC32header,            /** (I/O) ヘッダー部分のポインター **/
    int         * piNchannel,              /** (I/O) 全チャンネルヘッダーの個数 **/
    WIDECHAN **ppuiAll_channel,            /** ( O ) 全データに存在するチャンネル
                                            **       同じものは、はぶいてある **/
    int *piNall_channel                    /** ( O ) 全データに存在するチャンネルの総数
                                            **       **ppuiAll_channelの個数 **/
)
{
    int ia;
    int ib;
    /** 時刻・チャネル番号の順でソート **/
    for (ia=0; ia<*piNchannel; ia++) {
    }
    qsort((void *)*pptC32header, (size_t)*piNchannel, sizeof(C32_HEADER), (COMP) c32cmp1);
    for (ia=0; ia<*piNchannel; ia++) {
    }
    *ppuiAll_channel = (WIDECHAN *)calloc((size_t) *piNchannel,
                                                     sizeof(WIDECHAN));
    if (*ppuiAll_channel == NULL) {
        printf("***** ERROR ***** Memory alloc error.(c32datasort)\n");
        exit (0);
    }
    *piNall_channel = 0;
    for (ia=0; ia<*piNchannel; ia++) {
        if (*piNall_channel > 0) {
            for (ib=0; ib<*piNall_channel; ib++) {
                if (((*ppuiAll_channel)+ib)->uhChan0 == (*pptC32header+ia)->uhChanno0 &&
                    ((*ppuiAll_channel)+ib)->uhChan == (*pptC32header+ia)->uhChanno) break;
            }
            if (ib >= *piNall_channel) {
                ((*ppuiAll_channel)+*piNall_channel)->uhChan0 = (*pptC32header+ia)->uhChanno0;
                ((*ppuiAll_channel)+*piNall_channel)->uhChan = (*pptC32header+ia)->uhChanno;
                (*piNall_channel)++;
            }
        } else {
            ((*ppuiAll_channel)+*piNall_channel)->uhChan0 = (*pptC32header+ia)->uhChanno0;
            ((*ppuiAll_channel)+*piNall_channel)->uhChan = (*pptC32header+ia)->uhChanno;
            (*piNall_channel)++;
        }
    }
    qsort((void *)(*ppuiAll_channel), (size_t)*piNall_channel,
                                sizeof(WIDECHAN), (COMP) c32cmp2);
    for (ia=0; ia<*piNall_channel; ia++) {
    }
}

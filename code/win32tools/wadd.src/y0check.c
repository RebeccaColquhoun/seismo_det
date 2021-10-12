#include <y0wadd_n_man.h>
extern int giKbegin_main;
extern int giKbegin_sub;
extern int giKwin32_main;
extern int giKwin32_sub;
extern int giKwin32_both;
extern int giKwrite;
/** WIN32の時、先頭のフォーマット部を書いていない場合は書く **/
void check(
    int iSize,
    unsigned char * pucAdr
)
{
    int ia;
    int iFrame;
    int iBlock;
    int iAbuf[1000];
    int iKer;
    int iNsampno;
/*     int iii; */
    unsigned short uhChanno;
    for (ia=0; ia<8; ia++) {
    }
    pucAdr += 8;
    memmove(&iFrame, pucAdr, 4);
    swap4b((unsigned int *)&iFrame);
    pucAdr += 4;
    memmove(&iBlock, pucAdr, 4);
    swap4b((unsigned int *)&iBlock);
    pucAdr += 4;
    pucAdr++;
    pucAdr++;
    iKer = win2fix(                                /* チャンネルデータの全バイト数 */
        pucAdr,              /* ( I ) チャンネルデータ
                                         *      （チャンネル番号から） */
        iAbuf,                        /* ( O ) サンプルデータ */
        &uhChanno,          /* ( O ) チャンネル番号 */
        &iNsampno                      /* ( O ) サンプリング数 */
    );
    for (ia=0; ia<iNsampno; ia++) {
    }
}

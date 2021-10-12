#ifdef Module_Header
/*
* プログラム名：
*   blkcut
*
* 作者：松村
* 日付：1997/10/15
*
* 機能：
*   入力パラメータの前後のブランクまたはタブを削除し、出力パラメータにセットする。
*
* 簡易機能説明:
*   文字列の前後のブランクをカットする
*
* アーギュメント：
*   プログラム本体参照
*
*  戻り値：
*   なし
*
*
*
* 親：
*
* 子：
*
*/
#endif                                  /** #ifdef Module_Header **/
#include <string.h>
#include <v9dewin_prot.h>
void
blkcut(
    char *pcOut,                        /** ( O ) 前後のブランクまたはタブを削除した文字列 **/
    char *pcIn                          /** ( I ) 入力文字列 **/
)
{
    int     ia;
    int     ib;
    int     iSw;
    iSw = 0;
    for (ia = (int) strlen(pcIn) - 1; ia >= 0; ia--) {
        if (*(pcIn + ia) != ' ' && *(pcIn + ia) != '\t')
            break;
    }
    for (ib = 0; ib <= ia; ib++) {
        if (iSw == 0 &&
            (*(pcIn + ib) == ' ' || *(pcIn + ib) == '\t'))
            continue;
        *pcOut = *(pcIn + ib);
        iSw = 1;
        pcOut++;
    }
    *pcOut = '\0';
}

#ifdef Module_Header
/*
* �ץ����̾��
*   blkcut
*
* ��ԡ���¼
* ���ա�1997/10/15
*
* ��ǽ��
*   ���ϥѥ�᡼��������Υ֥�󥯤ޤ��ϥ��֤����������ϥѥ�᡼���˥��åȤ��롣
*
* �ʰ׵�ǽ����:
*   ʸ���������Υ֥�󥯤򥫥åȤ���
*
* ����������ȡ�
*   �ץ�������λ���
*
*  ����͡�
*   �ʤ�
*
*
*
* �ơ�
*
* �ҡ�
*
*/
#endif                                  /** #ifdef Module_Header **/
#include <string.h>
#include <v9dewin_prot.h>
void
blkcut(
    char *pcOut,                        /** ( O ) ����Υ֥�󥯤ޤ��ϥ��֤�������ʸ���� **/
    char *pcIn                          /** ( I ) ����ʸ���� **/
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

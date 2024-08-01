#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include <v9dewin_prot.h>
/************************************************************************
�ѥ�᡼�����ǻ��ꤵ�줿���Ƥ򸵤˽�����������ͥ��ֹ����롣
��������ޤ�����С������ͥ��ֹ椬ʣ�����ꤵ�줿�Ȥߤʤ���
���������ʿ����夤�ʤ��ʤ�С�ñ�ȤΥ����ͥ��ֹ椬���ꤵ�줿�Ȥߤʤ���
��������ʳ��ϡ������ͥ��ֹ�����ѤΥե����뤬���ꤵ�줿�Ȥߤʤ���
************************************************************************/
#define BUF_LEN  2048
extern unsigned int giKwidechan;
int
get_channel(
    char * pcParameter,                 /** ( I ) �ѥ�᡼���������� **/
    int  * piNchannel,                  /** ( O ) ����줿�����ͥ�ο� **/
    unsigned int **ppuiChid       /** ( O ) ����줿�����ͥ��ֹ� **/
)
{
    char * pc;
    int     iRet;
    int ia;
    static FILE * ptFile = NULL;
    char cOneline[BUF_LEN];
    char cOneline1[BUF_LEN];
    unsigned int uiWork;
    int     iKsw;
    char cWork[10];
    char * pc1;
    char * pc2;
    pc = strchr(pcParameter, ',');
    iRet = 1;
    pc2 = &cWork[0];
    pc1 = pcParameter;
    *piNchannel = 0;
    if (pc != NULL) {
        while (1) {
            pc = strtok(pc1, ",");
            if (pc != NULL) {
                if (giKwidechan == 0) {
                    if (strlen(pc) <= 0 || strlen(pc) > 4) goto ret;
                } else {
                    if (strlen(pc) <= 0 || strlen(pc) > 8) goto ret;
                }
                uiWork = strtoul(pc, &pc2, 16);
                if (pc2[0] != '\0') goto ret;
/*                 if (uiWork == INT_MAX || uiWork == INT_MIN) goto ret; */
                if (*piNchannel == 0) {
                    *ppuiChid = (unsigned int *)calloc(1, sizeof(unsigned int));
                } else {
                    *ppuiChid = realloc((void *)*ppuiChid, sizeof(unsigned int)*(*piNchannel+1));
                }
                *(*ppuiChid+(*piNchannel)) = (unsigned int)(uiWork);
                (*piNchannel)++;
            } else {
                break;
            }
            pc1 = NULL;
        }
    } else {
        iKsw = 0;
        if (strlen(pc1) <= 0) goto ret;
        if (giKwidechan == 0) {
            if (strlen(pc1) > 4) iKsw = 1;
        } else {
            if (strlen(pc1) > 8) iKsw = 1;
        }
        if (iKsw == 0) {
            uiWork = strtoul(pc1, &pc2, 16);
            if (pc2[0] != '\0') iKsw = 1;
            if (iKsw == 0) {
/*                 if (uiWork == INT_MAX || uiWork == INT_MIN) goto ret; */
                *ppuiChid = (unsigned int *)calloc(1, sizeof(unsigned int));
                *(*ppuiChid) = (unsigned int)(uiWork);
                (*piNchannel)++;
            }
        }
        /** �ե�����̾�� **/
        if (iKsw == 1) {
            if (ptFile != NULL) {
                fprintf(stderr, "%s file not close error.\n", pc1);
                exit(1);
            }
#ifdef MINGW
            ptFile = fopen(pc1,"r");
#else
            ptFile = fopen(pc1,"rt");
#endif
            if (ptFile == NULL) goto ret;
            while (fgets (cOneline1, BUF_LEN, ptFile) != 0) {
                if (cOneline1[strlen(cOneline1)-1] == '\n') {
                    cOneline1[strlen(cOneline1)-1] = '\0';
                }
                blkcut(cOneline, cOneline1);
                if (cOneline[0] == '\0') continue;
                if (cOneline[0] == '#') continue;
                pc1 = &cOneline[0];
                while (1) {
                    pc = strtok(pc1, ", \t");
                    if (pc == NULL) {
                        break;
                    } else {
                        if (strlen(pc) > 0 && pc[0] == '#') break;  /** ���ιԤ� **/
                        if (giKwidechan == 0) {
                            if (strlen(pc) <= 0 || strlen(pc) > 4) goto ret;
                        } else {
                            if (strlen(pc) <= 0 || strlen(pc) > 8) goto ret;
                        }
                        uiWork = strtoul(pc, &pc2, 16);
                        if (pc2[0] != '\0') goto ret;
/*                         if (uiWork == INT_MAX || uiWork == INT_MIN) goto ret; */
                        if (*piNchannel == 0) {
                            *ppuiChid = (unsigned int *)calloc(1, sizeof(unsigned int));
                        } else {
                            *ppuiChid = realloc((void *)*ppuiChid,
                                       sizeof(unsigned int)*(*piNchannel+1));
                        }
                        *(*ppuiChid+(*piNchannel)) = (unsigned int)uiWork;
                        (*piNchannel)++;
                    }
                    pc1 = NULL;
                }
            }
            fclose(ptFile);
            ptFile = NULL;
        }
    }
    iRet = 0;
ret:;
    for (ia=0; ia<*piNchannel; ia++) { 
/* printf("*(*ppuiChid+ia)=[%08x] (%s %d)\n", *(*ppuiChid+ia), __FILE__, __LINE__);  */
    }           
    return iRet; 
}

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
/************************************************************************
パラメーターで指定された内容を元に処理するチャンネル番号を求める。
１。カンマがあれば、チャンネル番号が複数指定されたとみなす。
２。１６進数４桁いないならば、単独のチャンネル番号が指定されたとみなす。
３。それ以外は、チャンネル番号指定用のファイルが指定されたとみなす。
************************************************************************/
void
blkcut(
    char *pcOut,                        /** ( O ) 前後のブランクまたはタブを削除した文字列 **/
    char *pcIn                          /** ( I ) 入力文字列 **/
);
#define BUF_LEN  2048
extern int giKwidechan;
int
get_channel(
    char * pcParameter,                 /** ( I ) パラメーターの内容 **/
    int  * piNchannel,                  /** ( O ) 得られたチャンネルの数 **/
    unsigned int **ppihChid             /** ( O ) 得られたチャンネル番号 **/
)
{
    char * pc;
    int     iRet;
    int ia;
    static FILE * ptFile = NULL;
    char cOneline[BUF_LEN];
    char cOneline1[BUF_LEN];
    int     iii;
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
                if (strlen(pc) <= 0 || strlen(pc) > 4) goto ret;
                iii = strtoul(pc, &pc2, 16);
                if (pc2[0] != '\0') goto ret;
                if (iii == INT_MAX || iii == INT_MIN) goto ret;
                if (*piNchannel == 0) {
                    *ppihChid = (unsigned int *)calloc(1, sizeof(unsigned int));
                } else {
                    *ppihChid = realloc((void *)*ppihChid, sizeof(unsigned int)*(*piNchannel+1));
                }
                *(*ppihChid+(*piNchannel)) = (unsigned int)(iii);
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
            iii = strtoul(pc1, &pc2, 16);
            if (pc2[0] != '\0') iKsw = 1;
            if (iKsw == 0) {
/*                 if (iii == INT_MAX || iii == INT_MIN) goto ret; */
                *ppihChid = (unsigned int *)calloc(1, sizeof(unsigned int));
                *(*ppihChid) = (unsigned int)(iii);
                (*piNchannel)++;
            }
        }
        /** ファイル名？ **/
        if (iKsw == 1) {
            if (ptFile != NULL) {
                fprintf(stderr, "%s file not close error.\n", pc1);
                exit(1);
            }
            ptFile = fopen(pc1,"r");
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
                        if (strlen(pc) > 0 && pc[0] == '#') break;  /** 次の行へ **/
                        if (giKwidechan == 0) {
                            if (strlen(pc) <= 0 || strlen(pc) > 4) goto ret;
                        } else {
                            if (strlen(pc) <= 0 || strlen(pc) > 8) goto ret;
                        }
                        iii = strtoul(pc, &pc2, 16);
                        if (pc2[0] != '\0') goto ret;
                        if (iii == INT_MAX || iii == INT_MIN) goto ret;
                        if (*piNchannel == 0) {
                            *ppihChid = (unsigned int *)calloc(1, sizeof(unsigned short int));
                        } else {
                            *ppihChid = realloc((void *)*ppihChid,
                                       sizeof(unsigned int)*(*piNchannel+1));
                        }
                        *(*ppihChid+(*piNchannel)) = (unsigned int)iii;
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
    }           
    return iRet; 
}

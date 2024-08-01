#ifndef C20_TYPE___H
#define C20_TYPE___H

#include <sys/types.h>
#ifdef MINGW
#include <stdio.h>
#include <fcntl.h>
#include <io.h>
#else
#include <unistd.h>
#endif

typedef int (*COMP) (const void *, const void *);

typedef struct __C20_HEADER {
    unsigned char ucStart[8];    /** ����ץ�󥰳���ǯ������ʬ�áܣ��������� **/
    int           iNframe;       /** �ե졼�����Ĺ�ʣ�������ñ�̡� **/
    unsigned short int uhChanno0; /** �ȿ�ID&�ȿ�����ID **/
    unsigned short int uhChanno; /** �����ͥ��ֹ� **/
#ifdef MINGW
    int           tOffset;       /** �ե�����Υ��ե��åȰ��� **/
#else
    off_t         tOffset;       /** �ե�����Υ��ե��åȰ��� **/
#endif
    int           iByte;         /** �Х��ȿ� **/
}       C32_HEADER;

typedef struct __WIDECHAN {
    unsigned short int uhChan0;  /** �ȿ�ID&�ȿ����� **/
    unsigned short int uhChan;   /** �����ͥ��ֹ� **/
}       WIDECHAN;

#endif  /** C20_TYPE___H **/

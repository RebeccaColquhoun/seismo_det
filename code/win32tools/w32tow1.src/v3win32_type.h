#ifndef V3WIN32_TYPE__H
#define V3WIN32_TYPE__H

typedef int (*COMP) (const void *, const void *);

typedef struct __WIN32_DATA {
    int iSeq;
    int iDate[8];
    int iFrlen;
    unsigned short int uhChanno;
    int iNbyte;
    unsigned char ucDat_date[8];
    unsigned char * pucWindata;
}       WIN32_DATA;

#endif

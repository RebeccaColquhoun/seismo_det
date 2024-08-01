#ifndef V8MKUTIL_MAN_HHHH
#define V8MKUTIL_MAN_HHHH
#include <stdio.h>
#include <string.h>
/*****************************/
/* 8/21/96 for little-endian (uehira) */
#ifndef         LITTLE_ENDIAN
#define LITTLE_ENDIAN   1234            /* LSB first: i386, vax */
#endif
#ifndef         BIG_ENDIAN
#define BIG_ENDIAN      4321            /* MSB first: 68000, ibm, net */
#endif
#ifndef  BYTE_ORDER
#define  BYTE_ORDER      BIG_ENDIAN
#endif

#define SWAPU  union { int l; float f; short s; char c[4];} swap
#define SWAPL(a) swap.l=(a); ((char *)&(a))[0]=swap.c[3];\
    ((char *)&(a))[1]=swap.c[2]; ((char *)&(a))[2]=swap.c[1];\
    ((char *)&(a))[3]=swap.c[0]
#define SWAPF(a) swap.f=(a); ((char *)&(a))[0]=swap.c[3];\
    ((char *)&(a))[1]=swap.c[2]; ((char *)&(a))[2]=swap.c[1];\
    ((char *)&(a))[3]=swap.c[0]
#define SWAPS(a) swap.s=(a); ((char *)&(a))[0]=swap.c[1];\
    ((char *)&(a))[1]=swap.c[0]
/*****************************/
#endif

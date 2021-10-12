#ifndef V9DEWIIIN_EXT_HHHH
#define V9DEWIIIN_EXT_HHHH

#include  <stdio.h>
#include  <signal.h>
#include  <math.h>
#include  <v9dewin_prot.h>

#define   DEBUG   0

#define PI          3.141592654
#define HP          (PI/2.0)
#define LINELEN     1024
#define MAX_SR      20000

/*****************************/
/* 5/16/98 for Little-Endian (uehira) */
#if 0
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
#define SWAPS(a) swap.s=(a); ((char *)&(a))[0]=swap.c[1];\
    ((char *)&(a))[1]=swap.c[0]
/*****************************/
#endif

extern int buf[MAX_SR];
extern double dbuf[MAX_SR];
extern unsigned int au_header[8];
extern int giKminutes;  /** 1:minutes file, 0:not minutes file **/
extern int giNsample;   /** sampling number (0>, <2000) **/

#endif

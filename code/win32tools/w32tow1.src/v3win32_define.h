#ifndef V3WIN32_DEFINE___H
#define V3WIN32_DEFINE___H

#define GS_MIN(a,b) (((a)<(b))?(a):(b)) /** �Ǿ��� **/
#define GS_MAX(a,b) (((a)>(b))?(a):(b)) /** ������ **/
#define GS_NINT(a) (((a)>0.0)?((int)((a)+0.5)):((int)((a)-0.5)))        /** �ͼθ��� **/
#define GS_NUMBER(arr)       ((int) (sizeof(arr) / sizeof(arr[0])))     /** ������礭�� **/
#define GS_OFFSETOF(s, m)    (int)(&(((s *)0)->m))                      /** ��¤�ΤΥ��ե��å� **/

#define GS_EPS_LEN 0.005                /** Ĺ���Υ��ץ���� **/
#define GS_EPS_DEG 0.005                /** ���٤Υ��ץ���� **/
#define GS_PAI     3.1415926535897932e0 /** �� **/

#endif

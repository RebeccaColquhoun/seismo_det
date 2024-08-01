#ifndef V3WIN32_DEFINE___H
#define V3WIN32_DEFINE___H

#define GS_MIN(a,b) (((a)<(b))?(a):(b)) /** 最小値 **/
#define GS_MAX(a,b) (((a)>(b))?(a):(b)) /** 最大値 **/
#define GS_NINT(a) (((a)>0.0)?((int)((a)+0.5)):((int)((a)-0.5)))        /** 四捨五入 **/
#define GS_NUMBER(arr)       ((int) (sizeof(arr) / sizeof(arr[0])))     /** 配列の大きさ **/
#define GS_OFFSETOF(s, m)    (int)(&(((s *)0)->m))                      /** 構造体のオフセット **/

#define GS_EPS_LEN 0.005                /** 長さのイプシロン **/
#define GS_EPS_DEG 0.005                /** 角度のイプシロン **/
#define GS_PAI     3.1415926535897932e0 /** π **/

#endif

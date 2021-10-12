/* $Id: winlib.h,v 1.1 1999/07/30 14:44:02 h-gotoh Exp h-gotoh $ */
/*
 * winlib.h -- win ライブラリヘッダーファイル
 *
 *     Copyright (C) 1999 By 白山工業株式会社
 *
 *     Author        : Hiroyuki Gotoh
 *     Last modified : Jul 30, 1999
 */

#ifndef _V8WINLIB_H_
#define _V8WINLIB_H_

#include <stdio.h>
#include <time.h>

#undef  WINLIB_VERSION
#define WINLIB_VERSION "0.9.8"

#undef  LSBFirst
#define LSBFirst 0
#undef  MSBFirst
#define MSBFirst 1

typedef unsigned char *WinData;
typedef unsigned short WinNumber;
typedef int WinValue;
typedef unsigned int WinSize;

#undef  MON_SR
#define MON_SR 5

typedef struct _ChParam {
    WinNumber ch_number;
    WinNumber smpl_size;
    WinNumber smpl_rate;
    WinNumber blk_size;
    WinData blk_ptr;
    WinNumber version;
}       ChParam, *ChParamList;

/* BitOper.c */
extern WinNumber Win_GetNumber(WinData);
extern WinSize Win_GetSize(WinData, WinNumber);
extern WinValue Win_GetValue(WinData, WinNumber);
extern WinValue Win_GetSeqValue(WinData, WinNumber);
extern WinValue Win_GetRevValue(WinData, WinNumber);
extern WinValue Win_GetValueB(WinData, WinNumber, WinNumber);
extern void Win_SetValue(WinValue, WinData, WinNumber);
extern void Win_SetSeqValue(WinValue, WinData, WinNumber);
extern void Win_SetRevValue(WinValue, WinData, WinNumber);
extern void
Win_SetValueB(WinValue, WinData,
    WinNumber, WinNumber);
extern WinValue Win_LimitValue(WinValue, WinNumber);
extern WinValue Win_LimitValueB(WinValue, WinNumber);
extern WinNumber Win_ReqBits(WinValue);
extern void Win_RevOrder(WinData, WinNumber, WinSize);
extern int Win_ByteOrder(void);

/* GetParam.c (requires BitOper.c) */
extern ChParam WinGetChParam(WinData);
extern ChParam WinMonGetChParam(WinData);
extern WinNumber WinGetChNumber(WinData);
extern WinNumber WinGetSmplSize(WinData);
extern WinNumber WinGetSmplRate(WinData);
extern WinNumber WinGetVersion(WinData);
extern WinNumber WinGetChSize(WinData);
extern WinNumber WinMonGetChSize(WinData);
extern WinNumber WinGetChParamList(WinData, WinSize, ChParamList *);
extern WinNumber WinMonGetChParamList(WinData, WinSize, ChParamList *);
extern WinData WinSearchChNumber(WinData, WinSize, WinNumber);
extern WinData WinMonSearchChNumber(WinData, WinSize, WinNumber);
extern  WinSize
WinSearchChList(WinData, WinSize,
    ChParamList, WinNumber);
extern  WinSize
WinMonSearchChList(WinData, WinSize,
    ChParamList, WinNumber);
extern WinValue WinGetRawValue(WinData, WinNumber);
extern  WinValue
WinMonGetRawValue(WinData, WinNumber,
    WinValue *, WinValue *);
extern WinValue WinGetOffset(WinData);
extern WinValue WinMonGetOffset(WinData);

/* Win2Pack.c (requires BitOper.c) */
extern WinSize Win2PkSec(WinData, WinSize, WinData);
extern WinSize Win2UpkSec(WinData, WinSize, WinData);
extern WinSize Win2PkSecSize(WinData, WinSize);
extern WinSize Win2UpkSecSize(WinData, WinSize);
extern WinNumber Win2PkCh(WinData, WinData);
extern WinNumber Win2UpkCh(WinData, WinData);
extern WinNumber Win2PkChSize(WinData);
extern WinNumber Win2UpkChSize(WinData);

/* BytePack.c (requires BitOper.c) */
extern WinNumber WinBytePkChSize(WinData, WinNumber, ChParam);
extern WinNumber WinBigEdPkChSize(WinData, WinNumber, ChParam);
extern WinNumber WinBytePkCh(WinData, WinNumber, ChParam, WinData);
extern WinNumber WinBigEdPkCh(WinData, WinNumber, ChParam, WinData);
extern WinNumber WinByteUpkCh(WinData, WinNumber, WinData);
extern WinNumber WinBigEdUpkCh(WinData, WinNumber, WinData);
extern WinNumber WinMonBytePkChSize(WinData, WinNumber, ChParam);
extern WinNumber WinMonBigEdPkChSize(WinData, WinNumber, ChParam);
extern WinNumber WinMonBytePkCh(WinData, WinNumber, ChParam, WinData);
extern WinNumber WinMonBigEdPkCh(WinData, WinNumber, ChParam, WinData);
extern WinNumber WinMonByteUpkCh(WinData, WinNumber, WinData);
extern WinNumber WinMonBigEdUpkCh(WinData, WinNumber, WinData);

/* Fileio.c (reqires BitOper.c, Time.c) */
extern WinSize WinReadSecHead(FILE *, int *);
extern WinSize WinWriteSecHead(FILE *, int *, WinSize);

/* Time.c */
extern WinData WinMkWinTime(int *, WinData);
extern int *WinMkIntTime(WinData, int *);
extern WinData WinMkCurTime(WinData);
extern WinData WinAddTime(WinData, time_t, WinData);
extern time_t WinDiffTime(WinData, WinData);
extern int WinEvalTime(WinData, WinData);
extern int WinTimeIsValid(WinData);

/* Clear.c */
extern WinSize WinClearSec(WinData, WinSize, WinData);
extern WinSize WinMonClearSec(WinData, WinSize, WinData);
extern WinNumber WinClearCh(WinData, WinData);
extern WinNumber WinMonClearCh(WinData, WinData);

extern void adj_time2(int *time);
extern int read_data(void);
extern int bcd_dec(int * dest, char * sour);
extern void bcd_dec8(int * dest, char * sour);
extern int time_cmp(int * t1, int * t2, int i);

#endif                                  /* _WINLIB_H_ */

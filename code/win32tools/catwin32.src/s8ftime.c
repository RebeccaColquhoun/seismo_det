#include <stdio.h>
#include <time.h>
#include <s8c32_prot.h>
void 
ftime_(int *iTime)
{
    time_t  sTime;
    struct tm *psTm;
    time(&sTime);
    psTm = localtime(&sTime);
    *(iTime + 0) = 1900 + psTm->tm_year;
    *(iTime + 1) = psTm->tm_mon + 1;
    *(iTime + 2) = psTm->tm_mday;
    *(iTime + 3) = psTm->tm_hour;
    *(iTime + 4) = psTm->tm_min;
    *(iTime + 5) = psTm->tm_sec;
    *(iTime + 6) = psTm->tm_wday;
}

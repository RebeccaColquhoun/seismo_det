#include <time.h>
void adj_time2(int *time)                            /* タイムスタンプのチェックを行
                                         * い 閏年閏秒の調整を行う */
{
    time_t t;
    struct tm *psTm;
    struct tm sTm;
    if (time[0] > 50) {
        sTm.tm_year = time[0];
    } else {
        sTm.tm_year = time[0]+100;
    }
    sTm.tm_mon = time[1] -1;
    sTm.tm_mday = time[2];
    sTm.tm_hour = time[3];
    sTm.tm_min = time[4];
    sTm.tm_sec = time[5];
    sTm.tm_wday = 0;
    sTm.tm_yday = 0;
    sTm.tm_isdst = 0;
    t = mktime(&sTm);
    psTm = localtime(&t);
    if (psTm->tm_year < 100) {
        *(time+0) = psTm->tm_year;
    } else {
        *(time+0) = psTm->tm_year - 100;
    }
    *(time+1) = psTm->tm_mon + 1;
    *(time+2) = psTm->tm_mday;
    *(time+3) = psTm->tm_hour;
    *(time+4) = psTm->tm_min;
    *(time+5) = psTm->tm_sec;
}

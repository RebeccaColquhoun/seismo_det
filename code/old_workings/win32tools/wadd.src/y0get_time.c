#include <time.h>
#include <y0wadd_prot.h>
int get_time(int * rt)                            /* ローカル時刻を獲得して６バイ
                                         * トの文字列(YYMMDDHHmmss)に */
{
    struct tm *nt;
    time_t ltime;
    time(&ltime);
    nt = localtime(&ltime);
    rt[0] = nt->tm_year % 100;
    rt[1] = nt->tm_mon + 1;
    rt[2] = nt->tm_mday;
    rt[3] = nt->tm_hour;
    rt[4] = nt->tm_min;
    rt[5] = nt->tm_sec;
    return 0;
}

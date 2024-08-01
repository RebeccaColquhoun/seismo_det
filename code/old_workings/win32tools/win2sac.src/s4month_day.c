#include <s4win2sac.h>
extern char daytab[2][13];
/* month_day */
void 
month_day(int year, int yearday, int *pmonth, int *pday)
{
    int     i, leap;
    leap = (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
    for (i = 0; yearday > daytab[leap][i]; i++)
        yearday -= daytab[leap][i];
    *pmonth = i;
    *pday = yearday;
}

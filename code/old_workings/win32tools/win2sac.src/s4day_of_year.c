#include <s4win2sac.h>
extern char daytab[2][13];
/* day of year */
int 
day_of_year(int year, int month, int day)
{
    int     i, leap;
    leap = 0;
    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0)
        leap = 1;
/*   leap = year%4 == 0 && year%100 != 0 || year%400 == 0; */
    for (i = 1; i < month; i++)
        day += daytab[leap][i];
    return day;
}

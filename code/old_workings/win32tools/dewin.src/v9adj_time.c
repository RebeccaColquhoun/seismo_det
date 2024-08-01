#include <v9dewin_ext.h>
int adj_time(int *tm)
{
    if (tm[5] == 60) {
        tm[5] = 0;
        if (++tm[4] == 60) {
            tm[4] = 0;
            if (++tm[3] == 24) {
                tm[3] = 0;
                tm[2]++;
                switch (tm[1]) {
                case 2:
                    if (tm[0] % 4 == 0) {
                        if (tm[2] == 30) {
                            tm[2] = 1;
                            tm[1]++;
                        }
                        break;
                    } else {
                        if (tm[2] == 29) {
                            tm[2] = 1;
                            tm[1]++;
                        }
                        break;
                    }
                case 4:
                case 6:
                case 9:
                case 11:
                    if (tm[2] == 31) {
                        tm[2] = 1;
                        tm[1]++;
                    }
                    break;
                default:
                    if (tm[2] == 32) {
                        tm[2] = 1;
                        tm[1]++;
                    }
                    break;
                }
                if (tm[1] == 13) {
                    tm[1] = 1;
                    if (++tm[0] == 100)
                        tm[0] = 0;
                }
            }
        }
    } else if (tm[5] == -1) {
        tm[5] = 59;
        if (--tm[4] == -1) {
            tm[4] = 59;
            if (--tm[3] == -1) {
                tm[3] = 23;
                if (--tm[2] == 0) {
                    switch (--tm[1]) {
                    case 2:
                        if (tm[0] % 4 == 0)
                            tm[2] = 29;
                        else
                            tm[2] = 28;
                        break;
                    case 4:
                    case 6:
                    case 9:
                    case 11:
                        tm[2] = 30;
                        break;
                    default:
                        tm[2] = 31;
                        break;
                    }
                    if (tm[1] == 0) {
                        tm[1] = 12;
                        if (--tm[0] == -1)
                            tm[0] = 99;
                    }
                }
            }
        }
    }
    return 0;
}

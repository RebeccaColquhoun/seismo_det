#include <string.h>
#include <y2wchch_man.h>
#include <y2wchch_prot.h>
typedef union __UNION_VAR
{
    unsigned int ui;
    int i;
} UNION_VAR;
int mkint(unsigned char * ptr)
{
    UNION_VAR uni;
    memmove(&uni.i, ptr, 4);
    swap4b((unsigned int *)&uni.ui);
    return uni.i;
}

#include <s4win2sac.h>
unsigned int 
mkint(unsigned char *ptr)
{
    unsigned char *ptr1;
    unsigned int a;
    ptr1 = (unsigned char *) &a;
    *ptr1++ = (*ptr++);
    *ptr1++ = (*ptr++);
    *ptr1++ = (*ptr++);
    *ptr1 = (*ptr);
    return a;
}

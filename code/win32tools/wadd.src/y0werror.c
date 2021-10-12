#include <stdlib.h>
#include <y0wadd_n_man.h>
int werror()
{
    perror("fwrite");
    exit(1);
}

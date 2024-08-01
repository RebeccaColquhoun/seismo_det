#include <string.h>
#include <y1wch_n_man.h>
#include <y1wch_prot.h>
#include <stdlib.h>
#ifdef MINGW
#include <stdio.h>
#include <fcntl.h>
#include <io.h>
#endif
int     giKbegin;
int     giKwin32;
int     giKwrite;
void ctrlc();
int main(int argc, char *argv[])
{
/*     static char ver[] = "@(#)wch_32(NIED) Ver 1.10 2003/06/03"; */
/*     static char ver[] = "@(#)wch_32(NIED) Ver 1.20 2003/11/10"; */
/*     static char ver[] = "@(#)wch_32(NIED) Ver 1.50 2007/12/20"; */
    int ia;
    int nn;
#ifdef MINGW
    int result;
#endif
#ifdef MINGW
   /* "stdin" をバイナリ モードに設定します。 */
    result=_setmode(_fileno(stdin),_O_BINARY);
    if( result == -1 ) {
        fprintf(stderr, "***** ERROR ***** The mode does not set.(%s %d)\n",
                __FILE__, __LINE__);
       exit(0);
    }
   /* "stdout" をバイナリ モードに設定します。 */
    result = _setmode( _fileno( stdout ), _O_BINARY );
    if( result == -1 ) {
        fprintf(stderr, "***** ERROR ***** The mode does not set.(%s %d)\n",
                __FILE__, __LINE__);
       exit(0);
    }
#endif
/*     fprintf(stderr, "%s\n", ver); */
    giKwrite = 0;
    giKbegin = 1;                       /* It has never been read yet. */
    giKwin32 = 0;                       /* The matter that it is not
                                         * WIN32 is set up. */
    giKbigchno = -1;
    for (ia=0; ia<argc; ia++) {
        if (strcmp(argv[ia], "-w") == 0 || strcmp(argv[ia], "-W") == 0 || strcmp(argv[ia], "-Y") == 0) {
            giKbigchno = ia;
            break;
        }
    }
    if (giKbigchno != -1) {
        nn = 0;
        for (ia=0; ia<argc; ia++) {
            if (ia == giKbigchno) continue;
            argv[nn] = argv[ia];
            nn++;
        }
        argc = nn;
    }
    signal(SIGINT, ctrlc);
    signal(SIGTERM, ctrlc);
    if (argc < 2) {
        fprintf(stderr, " usage of 'wch_32' :\n");
        fprintf(stderr, "   'wch_32 [-w|-W|-Y] ch_file < in_file > out_file'\n");
        exit(0);
    }
    if (read_chfile(argv[1]) > 0) {
        get_one_record();
    }
    exit(0);
}

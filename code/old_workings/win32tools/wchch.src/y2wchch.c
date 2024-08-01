#ifdef MINGW
#include <fcntl.h>
#include <io.h>
#endif
#include <y2wchch_man.h>
#include <y2wchch_prot.h>
#include <stdlib.h>
#include <string.h>
int     giKbegin;
int     giKwin32;
int     giKwrite;
int     giKwidechan;
void ctrlc();
int main(int argc, char *argv[])
{
#ifdef MINGW
    int result;
#endif
/*     static char ver[] = "@(#)wchch_32(NIED) Ver 1.10 2002/06/03"; */
/*     static char ver[] = "@(#)wchch_32(NIED) Ver 1.50 2007/12/20"; */
    int ia;
    int argcw;
    char *argvw[20];
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
    signal(SIGINT, ctrlc);
    signal(SIGTERM, ctrlc);
    giKwidechan = 0;
    argcw = 0;
    for (ia=0; ia<argc; ia++) {
        if (strcmp(argv[ia], "-Y") == 0) {
            giKwidechan = 1;
            continue;
        } else {
            argvw[argcw] = argv[ia];
            argcw++;
        }
    }
    if (argcw < 2) {
        fprintf(stderr, " usage of 'wchch_32' :\n");
        fprintf(stderr, "   'wchch_32 [-Y] [ch conv table] <[in_file] >[out_file]'\n");
        exit(0);
    }
    if (read_chfile(argvw[1]) > 0) {
        get_one_record();
    }
    exit(0);
}

#include <stdlib.h>
#include <string.h>
#ifdef MINGW
#include <fcntl.h>
#include <io.h>
#endif
#include <v8wed_man.h>
int     giKbegin;
int     giKwin32;
int     giKwrite;
int     giKnohead;
int     giKwidechan;
void ctrlc();
int 
main(argc, argv)
    int     argc;
    char   *argv[];
{
#ifdef MINGW
    int result;
#endif
    int     ia;
    int     argcw;
    char    *argvw[50];
/*     static char ver[] = "@(#)wed_32(NIED) Ver 1.10 2003/06/03"; */
/*     static char ver[] = "@(#)wed_32(NIED) Ver 1.50 2007/12/20"; */
/*     fprintf(stderr, "%s\n", ver); */
    giKwrite = 0;
    giKbegin = 1;                       /* It has never been read yet. */
    giKwin32 = 0;                       /* The matter that it is not
                                         * WIN32 is set up. */
    signal(SIGINT, ctrlc);
    signal(SIGTERM, ctrlc);
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
    giKwidechan = 0;
    argcw = 0;
    for (ia=0; ia<argc; ia++) {
        if (strcmp(argv[ia], "-Y") == 0) {
            giKwidechan = 1;
        } else {
            argvw[argcw] = argv[ia];
            argcw++;
        }
    }
    giKnohead = 0;
/*     for (ia=0; ia<argc; ia++) { */
/*         argvw[ia] = argv[ia]; */
/*     } */
/*     argcw = argc; */
    if (argc >= 2) {
        if (strcmp(argvw[1], "-nohead") == 0) {
            giKnohead = 1;
            if (argc >= 3) {
                for (ia=0; ia<argc-2; ia++) {
                    argvw[ia+1] = argvw[ia+2];
                }
            }
            argcw = argc-1;
        }
    }
    if (argcw < 4) {
        fprintf(stderr, " usage of 'wed_32' :\n");
        fprintf(stderr, "   'wed_32 [-Y] [YYMMDD] [hhmmss] [len(s)] ([ch list file]) <[in_file] >[out_file]'\n");
        fprintf(stderr, " example of channel list file :\n");
        fprintf(stderr, "   '01d 01e 01f 100 101 102 119 11a 11b'\n");
        exit(0);
    }
    if (argcw > 4) {
fprintf(stderr, "----- wed argvw[4] = [%s]\n", argvw[4]);
        if ((f_param = fopen(argvw[4], "r")) == NULL) {
            perror("fopen");
            exit(1);
        }
        nch = 0;
        while (fscanf(f_param, "%x", &guiSysch[nch]) != EOF) {
            nch++;
        }
        fclose(f_param);
    } else {
        nch = (-1);
    }
fprintf(stderr, "----- wed argvw[1] = [%s]\n", argvw[1]);
fprintf(stderr, "----- wed argvw[2] = [%s]\n", argvw[2]);
fprintf(stderr, "----- wed argvw[3] = [%s]\n", argvw[3]);
    sscanf(argvw[1], "%2d%2d%2d", dec_start, dec_start + 1, dec_start + 2);
    sscanf(argvw[2], "%2d%2d%2d", dec_start + 3, dec_start + 4, dec_start + 5);
    sscanf(argvw[3], "%d", &leng);
    get_one_record();
    exit(0);
}

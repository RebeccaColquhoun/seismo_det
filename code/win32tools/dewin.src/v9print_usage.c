#include <v9dewin_ext.h>
int print_usage()
{
    fprintf(stderr, "usage: dewin_32 [-m] [-s samp] [-c] [-a] [-n] [-e extend] [-f filter_file] ch_no [input_file]\n");
    fprintf(stderr, "        -m  Win file is minutes file.\n");
    fprintf(stderr, "        -s  [samp] sampling number.\n");
    fprintf(stderr, "        -c  character output\n");
    fprintf(stderr, "        -a  audio format (u-law) output\n");
    fprintf(stderr, "        -n  not fill absent part\n");
    fprintf(stderr, "        -e  [extend] file extend name\n");
    fprintf(stderr, "        -f  [filter_file] filter paramter file\n");
    fprintf(stderr, "     ch_no  channel no.(in hex.) or channel no. file name\n");
    fprintf(stderr, "input_file  input win file(default=stdin)\n");
    return 0;
}

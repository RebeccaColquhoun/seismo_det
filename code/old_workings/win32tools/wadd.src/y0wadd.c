#include <unistd.h>
#include <stdlib.h>
#include <y0wadd_n_man.h>
/* program "wadd.c"
  "wadd" puts two win data files together
  7/24/91 - 7/25/91, 4/20/94,6/27/94-6/28/94,7/12/94   urabe
        rindex -> strrchr 5/29/96
        97.8.14 remove duplicated channels from joined ch file
  98.6.26 yo2000
  98.7.1 FreeBSD
  99.5.1 devide program and create makefile by nishiyama
*/
int giKbegin_main;
int giKbegin_sub;
int giKwin32_main;
int giKwin32_sub;
int giKwin32_both;
int giKwrite;
int giKwidechan;
int main(int argc, char *argv[])
{
    int argcw;
    char *argvw[100];
    char * pcArgv3;
    char * pcDir;
    char * pcFnam;
    int     iii;
    int     ia;
    int    *piTime1;
    int    *piTime2;
    int     re, size, mainsize, subsize, init, mainend, subend, nch, dec_start[8], dec_now[8];
    FILE   *f_main, *f_sub, *f_out, *fp;
    char   *ptr;
    static unsigned char mainbuf[MAXSIZE], subbuf[MAXSIZE], tmpfile1[NAMLEN];
    static unsigned char textbuf[NAMLEN], new_file[NAMLEN], selbuf[MAXSIZE];
    static unsigned char tmpfile3[NAMLEN], chfile1[NAMLEN], chfile2[NAMLEN], tmpfile2[NAMLEN];
    static unsigned int sys_ch[65536];
/*     static char ver[] = "@(#)wadd_32(NIED) Ver 1.10 2003/06/03"; */
/*     static char ver[] = "@(#)wadd_32(NIED) Ver 1.20 2004/09/13"; */
/*     static char ver[] = "@(#)wadd_32(NIED) Ver 1.50 2007/12/20"; */
/*     fprintf(stderr, "%s\n", ver); */
    giKbegin_main = 1;  
    giKbegin_sub = 1; 
    giKwin32_main = 0;
    giKwin32_sub = 0; 
    giKwin32_both = 0; 
    giKwrite = 0; 
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
    if (argcw < 3) {
        fprintf(stderr, " usage of 'wadd_32' :\n");
        fprintf(stderr, "   wadd_32 [-Y] [main file] [sub file] ([output directory])\n");
        fprintf(stderr, "   -Y   wide chanel\n");
        fprintf(stderr, "   \n");
        fprintf(stderr, "   output file has the same name as 'main file'\n");
        exit(0);
    }
    if ((f_main = fopen(argvw[1], "rb")) == NULL) {
        perror("fopen");
        exit(1);
    }
    sprintf((char *)chfile1, "%s.ch", argvw[1]);
    if ((fp = fopen((char *)chfile1, "r")) == NULL) {
        *chfile1 = 0;
    } else {
        fclose(fp);
    }
    if ((f_sub = fopen(argvw[2], "rb")) == NULL) {
        perror("fopen");
        exit(1);
    }
    sprintf((char *)chfile2, "%s.ch", argvw[2]);
    if ((fp = fopen((char *)chfile2, "r")) == NULL) {
        *chfile2 = 0;
    } else {
        fclose(fp);
    }
    if (argcw > 3) {
        pcArgv3 = strdup(argvw[3]);
        if (pcArgv3[strlen(pcArgv3)-1] == '/') pcArgv3[strlen(pcArgv3)-1] = '\0';
        sprintf((char *)tmpfile1, "%s/%s.%d", pcArgv3, TEMPNAME, (int)getpid());
        sprintf((char *)tmpfile2, "%s/%s_ch.%d", pcArgv3, TEMPNAME, (int)getpid());
        sprintf((char *)tmpfile3, "%s/%s_chs.%d", pcArgv3, TEMPNAME, (int)getpid());
    } else {
        pcArgv3 = strdup("");
        sprintf((char *)tmpfile1, "%s.%d", TEMPNAME, (int)getpid());
        sprintf((char *)tmpfile2, "%s_ch.%d", TEMPNAME, (int)getpid());
        sprintf((char *)tmpfile3, "%s_chs.%d", TEMPNAME, (int)getpid());
    }
    if ((f_out = fopen((char *)tmpfile1, "w+b")) == NULL) {
        perror("fopen");
        exit(1);
    }
    init = 1;
    mainend = subend = 0;
    if ((mainsize = read_data_main(mainbuf, f_main)) == 0) {
        mainend = 1;
        nch = 0;
    } else {
        bcd_dec(dec_start, (char *) mainbuf + 4);
        nch = get_sysch(mainbuf, sys_ch);
#if DEBUG
        printf("nch=%d\n", nch);
#endif
    }
    if ((subsize = read_data_sub(selbuf, f_sub)) == 0) {
        subend = 1;
    } else {
		if (giKwin32_both==0) { /* win形式の場合のみ読込時に重複チャネル除去 */
        	if ((subsize = elim_ch(sys_ch, nch, selbuf, subbuf)) <= 10) {
            	subend = 1;
        	} else {
            	bcd_dec(dec_now, (char *) subbuf + 4);
        	}
		} else {
			bcd_dec(dec_now, (char *) selbuf + 4);
		}
    }
    while (mainend == 0 || subend == 0) {
        if (mainend == 0 && subend == 0) {
            piTime1 = &dec_start[0];
            piTime2 = &dec_now[0];
            if (giKwin32_both) piTime1++;
            if (giKwin32_both) piTime2++;
            re = time_cmp(piTime1, piTime2, 6);
        } else {
            re = 2;
        }
#if DEBUG
        printf("main=%d sub=%d re=%d\n", mainend, subend, re);
#endif
        if (subend || re == (-1)) {     /* write main until sub comes */
            if (init) {
                if (subend) {
                    if (form_write(f_out) != 0) {
                        werror();
                    }
                    if (giKwin32_both) {
                        check(mainsize, mainbuf+4);
                        if ((re = fwrite(mainbuf+4, 1, mainsize, f_out)) == 0) {
                            werror();
                        }
                    } else {
                        if ((re = fwrite(mainbuf, 1, mainsize, f_out)) == 0) {
                            werror();
                        }
                    }
                } else {
					if (giKwin32_both == 0) {   /* win形式の場合のみダミーデータ連結 */
                    	make_skel(subbuf, selbuf);
                    	memmove(&iii, selbuf, 4);
                    	swap4b((unsigned int *)&iii);
                    	if (giKwin32_both) {
                        	size = mainsize + iii - 16;/* 改修により結果的に無効 */
                    	} else {
                        	size = mainsize + iii - 10;
                    	}
					} else {                    /* win32形式の場合ダミーデータ連結しない */
						size = mainsize;
					}
                    swap4b((unsigned int *)&size);
                    if (form_write(f_out) != 0) {
                        werror();
                    }
                    if (giKwin32_both) {
                        memmove(&iii, &size, 4);
                        swap4b((unsigned int *)&iii);
                        size = iii - 16;
                        memmove(&iii, &size, 4); 
                        swap4b((unsigned int *)&iii);
                        memmove(mainbuf+16, &iii, 4);
                        check(mainsize, mainbuf+4);
                        if ((re = fwrite(mainbuf + 4, 1, mainsize, f_out)) == 0) {
                            werror();
                        }
/* win32形式の場合ダミーデータ連結しない
 *                        memmove(&iii, selbuf, 4); 
 *                        swap4b((unsigned int *)&iii);
 *                        check2(iii - 16, selbuf + 20);
 *                        memmove(&iii, selbuf, 4);
 *                        swap4b((unsigned int *)&iii);
 *                        if ((re = fwrite(selbuf + 20, 1, iii - 16, f_out)) == 0) {
 *                            werror();
 *                        }
 */
                    } else {
                        if ((re = fwrite(&size, 4, 1, f_out)) == 0) {
                            werror();
                        }
                        if ((re = fwrite(mainbuf + 4, 1, mainsize - 4, f_out)) == 0) {
                            werror();
                        }
                        memmove(&iii, selbuf, 4);
                        swap4b((unsigned int *)&iii);
                        if ((re = fwrite(selbuf + 10, 1, iii - 10, f_out)) == 0) {
                            werror();
                        }
                    }
                }
            } else {
                if (form_write(f_out) != 0) {
                    werror();
                }
                if (giKwin32_both) {
                    check(mainsize, mainbuf+4);
                    if ((re = fwrite(mainbuf+4, 1, mainsize, f_out)) == 0) {
                        werror();
                    }
                } else {
                    if ((re = fwrite(mainbuf, 1, mainsize, f_out)) == 0) {
                        werror();
                    }
                }
            }
            init = 0;
            if ((mainsize = read_data_main(mainbuf, f_main)) == 0) {
                mainend = 1;
            } else {
                bcd_dec(dec_start, (char *) mainbuf + 4);
				if (giKwin32_both != 0) {   /* win32の場合、チャネル取得 */
					memset(sys_ch, (int)NULL, sizeof(sys_ch));
					nch = get_sysch(mainbuf, sys_ch);
				}
            }
        } else if (mainend || re == 1) {/* skip sub until main */
            if (init == 0) {
                if (form_write(f_out) != 0) {
                    werror();
                }
                if (giKwin32_both) {
                    check(subsize, selbuf+4);
                    if ((re = fwrite(selbuf+4, 1, subsize, f_out)) == 0) {
                        werror();
                    }
                } else {
                    if ((re = fwrite(subbuf, 1, subsize, f_out)) == 0) {
                        werror();
                    }
                }
            }
            if ((subsize = read_data_sub(selbuf, f_sub)) == 0) {
                subend = 1;
            } else {
				if (giKwin32_both==0) { /* win形式の場合のみ読込時に重複チャネル除去 */
                	if ((subsize = elim_ch(sys_ch, nch, selbuf, subbuf)) <= 10) {
                    	subend = 1;
                	} else {
                    	bcd_dec(dec_now, (char *) subbuf + 4);
                	}
				} else {
					bcd_dec(dec_now, (char *) selbuf + 4);
				}
            }
        } else {                        /* start together */
            if (giKwin32_both) {
				/* win32形式の場合、マッチング後に重複チャネル除去 */
				if ((subsize = elim_ch(sys_ch, nch, selbuf, subbuf)) <= 16) {
                	size = mainsize;
				} else {
					size = mainsize + (subsize-16);
				}
           	} else {
               	size = mainsize + subsize - 10;
           	}
            swap4b((unsigned int *)&size);
            if (form_write(f_out) != 0) {
                werror();
            }
            if (giKwin32_both) {
                memmove(&iii, &size, 4);
                swap4b((unsigned int *)&iii);
                size = iii - 16;
                memmove(&iii, &size, 4);         
                swap4b((unsigned int *)&iii);        
                memmove(mainbuf+16, &iii, 4);
                check(mainsize, mainbuf+4);
                if ((re = fwrite(mainbuf + 4, 1, mainsize, f_out)) == 0) {
                    werror();
                }
				if (subsize > 16) {/* 重複除去した結果追加チャネルがある場合subファイル出力 */
                	check2(subsize - 16, subbuf + 20);
                	if ((re = fwrite(subbuf + 20, 1, subsize - 16, f_out)) == 0) {
                    	werror();
                	}
				}
            } else {
                if ((re = fwrite(&size, 4, 1, f_out)) == 0) {
                    werror();
                }
                if ((re = fwrite(mainbuf + 4, 1, mainsize - 4, f_out)) == 0) {
                    werror();
                }
                if ((re = fwrite(subbuf + 10, 1, subsize - 10, f_out)) == 0) {
                    werror();
                }
            }
            init = 0;
            if ((mainsize = read_data_main(mainbuf, f_main)) == 0) {
                mainend = 1;
            } else {
                bcd_dec(dec_start, (char *) mainbuf + 4);
				if (giKwin32_both != 0) {   /* win32の場合、チャネル取得 */
					memset(sys_ch, (int)NULL, sizeof(sys_ch));
					nch = get_sysch(mainbuf, sys_ch);
				}
            }
            if ((subsize = read_data_sub(selbuf, f_sub)) <= 10) {
                subend = 1;
            } else {
				if (giKwin32_both==0) { /* win形式の場合のみ読込時に重複チャネル除去 */
                	if ((subsize = elim_ch(sys_ch, nch, selbuf, subbuf)) <= 10) {
                    	subend = 1;
                	} else {
                    	bcd_dec(dec_now, (char *) subbuf + 4);
                	}
				} else {
					bcd_dec(dec_now, (char *) selbuf + 4);
				}
            }
        }
#if DEBUG
        printf("%02x%02x%02x%02x%02x%02x\n", mainbuf[4], mainbuf[5], mainbuf[6],
            mainbuf[7], mainbuf[8], mainbuf[9]);
        printf("%02x%02x%02x%02x%02x%02x\n", subbuf[4], subbuf[5], subbuf[6],
            subbuf[7], subbuf[8], subbuf[9]);
#endif
    }
    fclose(f_out);
    if ((ptr = strrchr(argvw[1], '/')) == NULL) {
        ptr = argvw[1];
        pcDir = strdup("");
    } else {
        *ptr = '\0';
        pcDir = strdup(argvw[1]);
        *ptr = '/';
        ptr++;
    }
    pcFnam = strdup(ptr);
    if (argcw > 3) {
        sprintf((char *)new_file, "%s/%s", pcArgv3, ptr);
    } else {
        strcpy((char *)new_file, ptr);
    }
    sprintf((char *)textbuf, "%s.sv", (char *)new_file);
    unlink((char *)textbuf);                    /* remove bitmap file if exists */
/*     if (strcmp(argvw[1], (char *)new_file)) { */
    if (strcmp(argvw[1], (char *)new_file) == 0) {
        rename((char *)tmpfile1, (char *)new_file);
    } else {
        sprintf((char *)textbuf, "cp %s %s", (char *)tmpfile1, (char *)new_file);
        system((char *)textbuf);
        unlink((char *)tmpfile1);
    }
    if (*chfile1 == 0 && *chfile2 == 0) {
/*         exit(0); */
    } else if (*chfile1) {
        sprintf((char *)textbuf, "cp %s %s", (char *)chfile1, (char *)tmpfile2);
        system((char *)textbuf);
        if (*chfile2) {
            sprintf((char *)textbuf, "grep -v '^#' %s|awk '{print $1}'>%s",
                     (char *)tmpfile2, (char *)tmpfile3);
            system((char *)textbuf);
            sprintf((char *)textbuf, "egrep -f %s -v %s >> %s",
                     (char *)tmpfile3, (char *)chfile2, (char *)tmpfile2);
            system((char *)textbuf);
        }
    } else if (*chfile2) {
        sprintf((char *)textbuf, "cp %s %s", (char *)chfile2, (char *)tmpfile2);
        system((char *)textbuf);
        system((char *)textbuf);
    }
    if (strcmp(argvw[1], (char *)new_file) == 0) {
        strcat((char *)new_file, ".ch");
        rename((char *)tmpfile2, (char *)new_file);
    } else {
        sprintf((char *)textbuf, "cp %s %s/%s.ch", (char *)tmpfile2, pcArgv3, pcFnam);
        system((char *)textbuf);
        unlink((char *)tmpfile2);
    }
    unlink((char *)tmpfile3);
    exit(0);
}

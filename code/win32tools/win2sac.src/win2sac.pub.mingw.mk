
CFLAGS = -I. -Wall -O3
CC  = gcc $(CFLAGS)

include win2sac.pub.mk.inc

OBJS2 = $(MMI_SRCS2:.c=.o)

.c.o:
	$(CC) -c $<


win2sac_32.exe:    $(OBJS2)
	$(CC) -o win2sac_32.exe $(OBJS2) -lm

clean:
	rm -f $(OBJS2) win2sac_32.exe



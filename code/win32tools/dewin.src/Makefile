
CFLAGS = -I. -Wall -O3
CC  = gcc $(CFLAGS)

include dewin.pub.mk.inc

OBJS2 = $(MMI_SRCS2:.c=.o)

.c.o:
	$(CC) -c $<


dewin_32:    $(OBJS2)
	$(CC) -o dewin_32 $(OBJS2) -lm

clean:
	rm -f $(OBJS2) dewin_32



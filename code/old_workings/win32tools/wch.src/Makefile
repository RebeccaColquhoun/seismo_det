
CFLAGS = -I. -Wall -O3
CC  = gcc $(CFLAGS)

include wch.pub.mk.inc

OBJS2 = $(MMI_SRCS2:.c=.o)

.c.o:
	$(CC) -c $<


wch_32:    $(OBJS2)
	$(CC) -o wch_32 $(OBJS2) -lm

clean:
	rm -f $(OBJS2) wch_32



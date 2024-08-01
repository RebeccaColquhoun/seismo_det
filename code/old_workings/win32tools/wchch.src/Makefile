
CFLAGS = -I. -Wall -O3
CC  = gcc $(CFLAGS)

include wchch.pub.mk.inc

OBJS2 = $(MMI_SRCS2:.c=.o)

.c.o:
	$(CC) -c $<


wchch_32:    $(OBJS2)
	$(CC) -o wchch_32 $(OBJS2) -lm

clean:
	rm -f $(OBJS2) wchch_32



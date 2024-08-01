
CFLAGS = -I. -DMINGW -Wall -O3
CC  = gcc $(CFLAGS)

include wchch.pub.mk.inc

OBJS2 = $(MMI_SRCS2:.c=.o)

.c.o:
	$(CC) -c $<


wchch_32.exe:    $(OBJS2)
	$(CC) -o wchch_32.exe $(OBJS2) -lm

clean:
	rm -f $(OBJS2) wchch_32.exe



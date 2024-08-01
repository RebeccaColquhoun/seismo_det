
CFLAGS = -I. -DMINGW -Wall -O3
CC  = gcc $(CFLAGS)

include wadd.pub.mk.inc

OBJS2 = $(MMI_SRCS2:.c=.o)

.c.o:
	$(CC) -c $<


wadd_32.exe:    $(OBJS2)
	$(CC) -o wadd_32.exe $(OBJS2) -lm

clean:
	rm -f $(OBJS2) wadd_32.exe



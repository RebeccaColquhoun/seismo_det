
CFLAGS = -I. -Wall -O3
CC  = gcc $(CFLAGS)

include wed.pub.mk.inc

OBJS2 = $(MMI_SRCS2:.c=.o)

.c.o:
	$(CC) -c $<


wed_32:    $(OBJS2)
	$(CC) -o wed_32 $(OBJS2) -lm

clean:
	rm -f $(OBJS2) wed_32



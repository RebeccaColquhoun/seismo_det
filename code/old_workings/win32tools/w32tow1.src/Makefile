
CFLAGS = -I. -Wall -O3
CC  = gcc $(CFLAGS)

include w32tow1.pub.mk.inc

OBJS2 = $(MMI_SRCS2:.c=.o)

.c.o:
	$(CC) -c $<


w32tow1:    $(OBJS2)
	$(CC) -o w32tow1 $(OBJS2) -lm

clean:
	rm -f $(OBJS2) w32tow1



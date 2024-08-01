
CFLAGS = -I. -DMINGW -Wall -O3
CC  = gcc $(CFLAGS)

include catwin32.pub.mk.inc

OBJS2 = $(MMI_SRCS2:.c=.o)

.c.o:
	$(CC) -c $<


catwin32:    $(OBJS2)
	$(CC) -o catwin32 $(OBJS2) -lm

clean:
	rm -f $(OBJS2) catwin32



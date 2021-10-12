
CFLAGS = -DMINGW -I. -Wall -O3
CC  = gcc $(CFLAGS)

include wck.pub.mk.inc

OBJS2 = $(MMI_SRCS2:.c=.o)

.c.o:
	$(CC) -c $<


wck_32.exe:    $(OBJS2)
	$(CC) -o wck_32.exe $(OBJS2) -lm

clean:
	rm -f $(OBJS2) wck_32.exe



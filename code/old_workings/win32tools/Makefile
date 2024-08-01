SUBDIRS = 	catwin32.src dewin.src w32tow1.src wadd.src wch.src wchch.src wck.src wed.src win2sac.src
MODULES = 	catwin32.src/catwin32 dewin.src/dewin_32 w32tow1.src/w32tow1 wadd.src/wadd_32 \
			wch.src/wch_32 wchch.src/wchch_32 wck.src/wck_32 wed.src/wed_32 win2sac.src/win2sac_32

all:
	for d in $(SUBDIRS); do \
		cd $$d; \
		$(MAKE); \
		cd ..; \
	done

clean:
	find . -name \*.o -exec rm '{}' \;

install:
	cp -fp $(MODULES) /usr/local/bin

CFLAGS+= -std=c99 -O3 -g -pedantic -Wall -Werror
HW=main
ZIP=zip

$(HW): main.c 
	$(CC) $(CFLAGS) main.c -o $(HW)

zip:
	$(ZIP) $(HW)-brute.zip main.c

clean:
	$(RM) *.o
	$(RM) $(HW)
	$(RM) $(HW)-brute.zip

.PHONY: clean zip

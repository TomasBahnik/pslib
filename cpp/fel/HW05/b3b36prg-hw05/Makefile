CFLAGS+=  clang -c main.c -std=c99 -g -pedantic -Wall -Werror  -o main.o
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

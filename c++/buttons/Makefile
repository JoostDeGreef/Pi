
all: buttons

buttons: buttons.c++ Makefile
	g++ -Wall -pthread -o buttons buttons.c++ -lpigpio -lrt
	
clean:
	rm -f *~ *.o buttons
	
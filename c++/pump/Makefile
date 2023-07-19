
all: pump

pump: main.cpp Makefile pigpio++.o
	g++ -Wall -pthread -o pump main.cpp -lpigpio -lrt pigpio++.o
	
pigpio++.o: Makefile pigpio++.hpp pigpio++.cpp
	g++ -Wall -pthread -o pigpio++.o -c pigpio++.cpp
	
clean:
	rm -f *~ *.o pump
	
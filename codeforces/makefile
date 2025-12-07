CC=g++
CFLAGS=-std=c++11 -O2 -Wall
DIR=
EXE=

MAINPATH=$(DIR)/$(EXE)

all: comp run

clean:
	rm -f a.out

comp:
	@echo "Compiling $(MAINPATH)"
	$(CC) $(CFLAGS) $(MAINPATH)/main.cpp -o a.out

run :
	@echo "----------------- Running $(MAINPATH) -----------------"
	./a.out < $(MAINPATH)/in

copy:
	@echo "Creating new directory for exercise $(MAINPATH)"
	mkdir $(MAINPATH)
	cp -R template/* $(MAINPATH)/

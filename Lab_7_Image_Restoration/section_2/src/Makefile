# For Linux or any machines with gcc compiler
CC = gcc
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: section_2

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o

section_2: section_2.o $(OBJ)
	$(CC) $(CFLAGS) -o section_2 section_2.o $(OBJ) -lm
	mv section_2 $(BIN)

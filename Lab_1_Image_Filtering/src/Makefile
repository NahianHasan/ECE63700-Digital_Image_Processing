# For Linux or any machines with gcc compiler
CC = gcc
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: FIR_LP_4 FIR_Sharp_3 IIR_3

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o

FIR_LP_4: FIR_LP_4.o $(OBJ)
	$(CC) $(CFLAGS) -o FIR_LP_4 FIR_LP_4.o $(OBJ) -lm
	mv FIR_LP_4 $(BIN)

FIR_Sharp_3: FIR_Sharp_3.o $(OBJ)
	$(CC) $(CFLAGS) -o FIR_Sharp_3 FIR_Sharp_3.o $(OBJ) -lm
	mv FIR_Sharp_3 $(BIN)

IIR_3: IIR_3.o $(OBJ)
	$(CC) $(CFLAGS) -o IIR_3 IIR_3.o $(OBJ) -lm
	mv IIR_3 $(BIN)


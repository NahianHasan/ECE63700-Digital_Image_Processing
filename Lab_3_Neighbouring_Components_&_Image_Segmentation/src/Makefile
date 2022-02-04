# For Linux or any machines with gcc compiler
CC = gcc
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: connected_components connected_components_single_pixel

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o

connected_components_single_pixel: connected_components_single_pixel.o $(OBJ)
	$(CC) $(CFLAGS) -o connected_components_single_pixel connected_components_single_pixel.o $(OBJ) -lm
	mv connected_components_single_pixel $(BIN)

connected_components: connected_components.o $(OBJ)
	$(CC) $(CFLAGS) -o connected_components connected_components.o $(OBJ) -lm
	mv connected_components $(BIN)

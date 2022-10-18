CC = gcc
LIB_DIR = lib

default: pyexamples

main:
	$(CC) main.c -o main

pyexamples: setup.py pyexamples.pyx $(LIB_DIR)/libhello.a
	python3 setup.py build_ext --inplace && rm -f pyexamples.c && rm -Rf build

$(LIB_DIR)/libhello.a:
	make -C $(LIB_DIR) libhello.a

clean:
	rm main *.so

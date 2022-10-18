## C Library callable from Python by wrapping it with Cython

1. Probando main.c:
```
make main
./main
```

2. Compilando Library:
```
cd lib
make
```

3. Build the module:
```
make
```

4. Probar:
```
python main.py
```


Based on https://stavshamir.github.io/python/making-your-c-library-callable-from-python-by-wrapping-it-with-cython/

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

3. Instalar cython:
```
conda create -n cython python=3.8 -y
conda activate cython
pip install cython
```

4. Build the module:
```
make
```

5. Probar:
```
python main.py
```


Based on https://stavshamir.github.io/python/making-your-c-library-callable-from-python-by-wrapping-it-with-cython/

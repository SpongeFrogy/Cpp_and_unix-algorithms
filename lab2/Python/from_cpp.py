# python 3.7.15
from ctypes import*

mydll = windll.LoadLibrary('C:/Users/droid/Projects/6sem_Cpp_and_unix/lab2/C++/for_python/shared_lib.dll')

mydll.func.restype = c_double

result2 = mydll.func(100,1000000)

print(type(result2))

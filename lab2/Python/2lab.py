import numpy as np
import timeit

x = np.random.random()

def func(x):
    return x ** 2 - x ** 2 + x * 4 - x * 5 + x + x

n = int(input('ВВедите кол-во повтоений:'))

time = timeit.timeit(stmt='func(x)', globals={"func": func, "x": x}, number=n)

print("%.5f sec." %time)




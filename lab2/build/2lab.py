import numpy as np
import timeit

x = np.random.random()

def func(x):
    return x ** 2 - x ** 2 + x * 4 - x * 5 + x + x

def time_exp():
    inputn = input('Enter the number of loops:')
    try:
        n = int(inputn)
        print('Thats int.')
    except ValueError:
        print('Thats not int.')
        return None
    time = timeit.timeit(stmt='func(x)', globals={"func": func, "x": x}, number=n)
    return (n, time)

while True:
    res = time_exp()
    if res == None:
        break
    print("Time of %i loops is %.2e sec."%res)
    answer = str(input('again [y/n]?'))
    if answer != 'y':
        break 



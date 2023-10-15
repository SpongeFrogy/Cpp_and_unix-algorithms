from timeit import timeit

# url https://proglib.io/p/slozhnost-algoritmov-i-operaciy-na-primere-python-2020-11-03


a = list(range(1000))

n = 100000

t1 = timeit(stmt="[a[i] for i in range(100)]", globals=globals(), number=n)

t2 = timeit(stmt="a[:100]", globals=globals(), number=n)

print(f"time with item by item: {t1:.2f} s. for {n} iterations \ntime with slice: {t2:.2f} s. for {n} iterations")

# * time with item by item: 9.29 s. for 100000 iterations 
# * time with slice: 2.07 s. for 100000 iterations


# ! binary operators
# url https://www.bestprog.net/ru/2019/10/21/python-bitwise-operators-ru/

i = 123

print(f"i = {bin(i)} \n~i = {bin(~i)}\n0<<i = {bin(0<<i)}\n1|i = {bin(1|i)}")


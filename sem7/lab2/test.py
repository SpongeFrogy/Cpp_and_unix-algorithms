from timeit import timeit

# https://proglib.io/p/slozhnost-algoritmov-i-operaciy-na-primere-python-2020-11-03

a = list(range(1000))

n = 100000

t1 = timeit(stmt="[a[i] for i in range(100)]", globals=globals())

t2 = timeit(stmt="a[:100]", globals=globals())

print(f"time with item by item: {t1:.2f} s. for {n} iterations \ntime with slice: {t2:.2f} s. for {n} iterations")

# time with item by item: 9.29 s. for 100000 iterations 
# time with slice: 2.07 s. for 100000 iterations


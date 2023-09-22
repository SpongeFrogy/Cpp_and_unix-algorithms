import numpy as np

INT_MAX = 1000
# m = np.array([[0, 0, 0, 0, 0],
#        [0, 0, 10, 15, 20],
#        [0, 10, 0, 25, 25],
#        [0, 15, 25, 0, 30],
#        [0, 20, 25, 30, 0]])


m = np.array([[0, 1, 2],
              [3, 0, 4],
              [5, 6, 0]])

def tsp(set: list[int], from_city: int) -> float:
    print(f"in set is {set}")
    if set == []:
        print("if ret")
        return 0
    distance = INT_MAX
    for city in set:
        #print(set)
        subset = set.copy()
        subset.remove(city)
        #print(subset)
        print(f"for {from_city} to {city}")
        sub_distance = m[from_city, city] + tsp(subset, city)
        if sub_distance < distance:
            distance = sub_distance
        print(f"{distance} from {from_city} to {city}")
    print("m ret")
    return distance

print(tsp(list(range(len(m))), 0))
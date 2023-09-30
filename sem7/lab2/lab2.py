import sys
import random
import numpy as np



class TriangularMatrix:
   def __init__(self, size: int) -> None:
      self.size = size
      self.matrix = [0.] * (size * (size + 1) // 2)

   def __setitem__(self, key: tuple[int, int], value) -> None:
      i, j = max(key), min(key)
      index = (i * (i + 1) // 2) + j
      self.matrix[index] = value
   
   def __getitem__(self, key: tuple[int, int]) -> None:
      i, j = max(key), min(key)
      index = (i * (i + 1) // 2) + j
      return self.matrix[index]
   
   # def __str__(self) -> str:
   #    s = ""
   #    for i in range(self.size):
   #       for j in range(i):
   #          s+= str(self.__getitem__((i, j))) + ", "
   #       s+= str(self.__getitem__((i, i)))
   #       s += "\n"
   #    return s
   
   def __str__(self) -> str:
      s = ""
      j = 0
      for i in range(1, self.size + 1):
         s+= (self.matrix[j:i+j].__str__()) + "\n"
         j += i
      return s

   def __len__(self) -> int:
      return self.size


def random_points(n: int, m=10) -> np.ndarray:
   return np.random.random((n, 2)) * m

def make_distance_matrix(points: np.ndarray) -> list[list[float]]:
   matrix = TriangularMatrix(points.shape[0])
   for i in range(len(points)):
      for j in range(len(points)):
         matrix[i, j] = np.linalg.norm(points[i] - points[j])
   return matrix

def tsp_recursive(graph, visited, current_city, start_city, num_cities):
   if visited == (1 << num_cities) - 1: # !  here
      # If all cities are visited, return to the start city
      return graph[current_city, start_city], [current_city, start_city]
    
   min_tour_cost = sys.maxsize
   min_path = []

   for next_city in range(num_cities):
      if not visited & (1 << next_city):  # !  here
         visited |= 1 << next_city  # !  here
         tour_cost, path = tsp_recursive(graph, visited, next_city, start_city, num_cities)
         tour_cost += graph[current_city, next_city]
            
         if tour_cost < min_tour_cost:
            min_tour_cost = tour_cost
            min_path = [current_city] + path
            
         visited &= ~(1 << next_city)  # !  here
    
   return min_tour_cost, min_path

def tsp(graph: list[list[float]]) -> tuple[float, list[int]]:
   num_cities = len(graph)
   start_city = 0
   visited = 1 << start_city
   min_tour_cost, min_path = tsp_recursive(graph, visited, start_city, start_city, num_cities)
    
   return min_tour_cost, min_path

graph = [[  0,  0,  0,  0,  0],
         [  0,  0, 10, 15, 20],
         [  0, 10,  0, 25, 25],
         [  0, 15, 25,  0, 30],
         [  0, 20, 25, 30,  0]]

g = TriangularMatrix(5)

for i in range(5):
   g[i,i] = graph[i][i]
   for j in range(i):
      g[i, j] = graph[i][j]

points = random_points(5)
g_2 = make_distance_matrix(points)

print(g)

min_tour_cost = tsp(g)
print("Minimum TSP Tour Cost:", min_tour_cost)
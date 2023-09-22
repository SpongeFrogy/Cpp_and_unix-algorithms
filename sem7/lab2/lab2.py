import sys
import random




def random_points(n: int, m=10) -> list[list[float]]:
   points = [[0., 0.]]*n
   for i in range(n):
      for j in range(2):
         points[i][j] = random.random() * m
   return points

def make_distance_matrix(points: list[list[float]]) -> list[list[float]]:
   matrix = [[0.]*len(points)]*len(points)
   for i in range(len(points)):
      for j in range(len(points)):
         matrix[i][j] = ((points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2)**0.5
         print(points[i][0])
   return matrix

def tsp_recursive(graph, visited, current_city, start_city, num_cities):
   if visited == (1 << num_cities) - 1:
      # If all cities are visited, return to the start city
      return graph[current_city][start_city], [current_city, start_city]
    
   min_tour_cost = sys.maxsize
   min_path = []

   for next_city in range(num_cities):
      if not visited & (1 << next_city):
         visited |= 1 << next_city
         tour_cost, path = tsp_recursive(graph, visited, next_city, start_city, num_cities)
         tour_cost += graph[current_city][next_city]
            
         if tour_cost < min_tour_cost:
            min_tour_cost = tour_cost
            min_path = [current_city] + path
            
         visited &= ~(1 << next_city)
    
   return min_tour_cost, min_path

def tsp(graph: list[list[float]]) -> tuple[float, list[int]]:
   num_cities = len(graph)
   start_city = 0
   visited = 1 << start_city
   min_tour_cost, min_path = tsp_recursive(graph, visited, start_city, start_city, num_cities)
    
   return min_tour_cost, min_path

# Example usage:
graph = [       [  0,  0,  0,  0,  0],
                [  0,  0, 10, 15, 20],
                [  0, 10,  0, 25, 25],
                [  0, 15, 25,  0, 30],
                [  0, 20, 25, 30,  0]]

# points = random_points(4)
# print(points)
# graph = make_distance_matrix(points)

# print(graph)

min_tour_cost = tsp(graph)
print("Minimum TSP Tour Cost:", min_tour_cost)

#print(sum([graph[0][3], graph[3][1], graph[1][2], graph[2][4], graph[4][0]]))
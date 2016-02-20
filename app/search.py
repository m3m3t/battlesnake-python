import collections
import ctypes
from multiprocessing import Process as _Process, Array as _Array
import numpy as _np

class SimpleGraph:
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, id):
        return self.edges[id]

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snakes = [] #list of x,y coordinates
    
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id):
        return id not in self.snakes
    
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def pad_arr(vector, pad_width, iaxis, kwargs):
        vector[:pad_width[0]] = 0
        vector[-pad_width[1]:] = 0
        return vector

    def cost(from_node, to_node):
        return 1

import heapq
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def heuristic(a, b, D, _type='manhattan'):
    (x1, y1) = a
    (x2, y2) = b
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    if _type == 'manhattan':
        return D * (dx + dy)
    elif _type == 'diagonal':
        D2 = 1
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy) 
    elif _type == 'euclidean':
        return D * (dx*dx + dy*dy)
        

def a_star_search(result, grid, start, goal):
    print result
    print grid
    print start
    print goal
    
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        print current  
        if current == goal:
            break
        
        for next in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, 1, next)
                frontier.put(next, priority)
                came_from[next] = current
   
    result[0] = came_from
    result[1] = cost_so_far
    print "Result:", result

def ping(grid, current, goals):
    shared_array_base = _Array(ctypes.c_int, 2)
    result = _np.ctypeslib.as_array(shared_array_base.get_obj())
    current = tuple(current) 
    """
    (r,c) = graph.shape

    h = int(r / 2)
    w = int(c / 2)

    subgraph = [(0,h,0,w),(0,h,w,c),(h,r,0,w),(h,r,w,c)]
    processes = [ _Process(target=a_star_search, args=(result, subgraph[i], current, goals[i])) for i in range(0,4) ]
    """
    goal = goals[0] 
    processes = [ _Process(target=a_star_search, args=(result, grid, current, goal)) ]
    
    for p in processes:
        p.start();

    for p in processes:
        p.join();
  
    return result

def get_move(grid, current, food):

    result = ping(grid, current, food) 
    
    return "north"


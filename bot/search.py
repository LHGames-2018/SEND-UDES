from queue import PriorityQueue


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = set()
        self.weights = dict()
    
    def in_bounds(self, coord):
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, coord):
        return coord not in self.walls
    
    def neighbors(self, coord):
        x, y = coord
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        return [c for c in results if self.in_bounds(c) and self.passable(c)]
    
    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for nxt in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, nxt)
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + heuristic(goal, nxt)
                frontier.put(nxt, priority)
                came_from[nxt] = current

    return came_from, cost_so_far

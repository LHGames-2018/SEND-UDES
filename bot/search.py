from queue import PriorityQueue

from helper import Point


class Grid:
    def __init__(self, width, height, players):
        self.width = width
        self.height = height
        self.players = players
        self.walls = set()
        self.resources = dict()
        self.resources_neighbours = set()
        self.weights = dict()
        self.house = Point()
    
    def in_bounds(self, coord):
        x, y = coord
        return -10 <= x < self.width and -10 <= y < self.height
    
    def passable(self, coord):
        return coord not in self.walls
    
    def neighbors(self, coord, goal):
        x, y = coord
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        return set(c for c in results if c == goal or (self.in_bounds(c) and self.passable(c)))
    
    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

    def a_star_search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            _, current = frontier.get()

            if current == goal:
                break

            for nxt in self.neighbors(current, goal):
                new_cost = cost_so_far[current] + self.cost(current, nxt)
                if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                    cost_so_far[nxt] = new_cost
                    priority = new_cost + heuristic(goal, nxt)
                    frontier.put((priority, nxt))
                    came_from[nxt] = current
            frontier.task_done()

        path = [goal]
        cur = goal
        while cur != start:
            path.append(cur)
            cur = came_from.get(cur, start)

        return path[-1]


def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)

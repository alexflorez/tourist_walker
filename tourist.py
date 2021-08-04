import numpy as np
from skimage import io
from collections import deque
from collections import defaultdict
from itertools import product

from environment import Environment


class Tourist:
    def __init__(self, space, mu, position, rule='min'):
        self.space = space
        # mu: number of visited cities
        self.mu = mu
        self.position = position
        self.rule = rule
        self.path = [self.position]
        self.cycle = []
        # Determine if cycle is found
        self.found = False
        self.visited = deque(maxlen=mu)
        self.visited.append(self.position)
        # To keep the occurrences of position along the path
        self.indexes = defaultdict(list)
        self.indexes[position].append(0)

    def next_position(self):
        positions = self.space.possibles(self.position, self.rule)
        for pos in positions:
            if pos not in self.visited:
                self.visited.append(pos)
                return pos
        # If it does not find a new position
        return self.position

    def find_indexes(self, point):
        idx = len(self.path)
        self.indexes[point].append(idx)
        return self.indexes[point]

    def step(self):
        point = self.next_position()
        # It can't move to another position, cycle is empty
        if self.position == point:
            self.found = True
            return

        indexes = self.find_indexes(point)
        # check presence of cycle
        for ix in indexes[:-1]:
            cycle = self.path[ix:]
            elems = len(cycle)
            subpath = self.path[ix - elems: ix]
            if cycle == subpath:
                self.cycle = cycle
                self.found = True
                return

        self.position = point
        self.path.append(self.position)

    def traverse(self):
        while not self.found:
            self.step()
        cycle = len(self.cycle)
        path = len(self.path) - 2 * cycle
        return path, cycle


def traverse_environment(space, mu, rule="min"):
    m, n = space.data.shape
    n_points = m * n
    measures = 2
    transient_cycle = np.empty((n_points, measures), dtype=int)
    for k, (i, j) in enumerate(product(range(m), range(n))):
        point = (i, j)
        tourist = Tourist(space, mu, point, rule)
        path, cycle = tourist.traverse()
        transient_cycle[k] = [path, cycle]
    return transient_cycle


if __name__ == "__main__":
    file = "data/image.png"
    mu_visits = 2
    rule_dir = "max"
    image = io.imread(file)
    env = Environment(image)
    dt = traverse_environment(env, mu_visits, rule_dir)
    print(dt)

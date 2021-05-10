from skimage import io
from skimage import transform
from collections import deque
from itertools import product

from environment import Environment, Point


class Tourist:
    def __init__(self, space, mu, position):
        self.space = space
        # mu: number of visited cities
        self.mu = mu
        self.position = position
        self.path = [self.position]
        self.cycle = []
        self.found = False
        self.visited = deque(maxlen=mu)
        self.visited.append(self.position)

    def next(self):
        indexes, shape = self.space.possibles(self.position)
        for i in indexes:
            dx, dy = shape[i]
            x, y = self.position
            pos = Point(x + dx, y + dy)
            if pos not in self.visited:
                return pos
        # if it does not find a new position
        return self.position

    def step(self):
        # if it was already found a cycle
        if self.found:
            return self.found

        pos = self.next()
        if self.position == pos:
            return self.found
        self.position = pos
        self.visited.append(pos)
        if pos not in self.path:
            if pos not in self.cycle:
                self.path.extend(self.cycle)
                self.cycle.clear()
            self.path.append(pos)
        else:
            # last occurrence of element
            k = self.path[::-1].index(pos)
            # updating to actual index
            k = len(self.path) -k - 1
            if pos in self.cycle and pos == self.cycle[0]:
                self.found = True
            elif not self.cycle:
                self.cycle.append(pos)
            elif self.cycle[-1] == self.path[k - 1]:
                self.cycle.append(pos)
            else:
                # it was found an element that breaks the possible cycle
                self.path.extend(self.cycle)
                self.path.append(pos)
                self.cycle.clear()
        return self.found


def test_one_path(file, shape_neighbors, n_visits):
    image = io.imread(file, as_gray=True)
    x_size, y_size = 100, 100
    image = transform.resize(image, (x_size, y_size), anti_aliasing=True)
    space = Environment(image, shape_neighbors)
    m, n = space.data.shape
    n_features = m * n
    i, j = 49, 10
    point = Point(i, j)
    tourist = Tourist(space, n_visits, point)
    for k in range(n_features):
        tourist.step()
        if tourist.found:
            break
    print(f"{tourist.found} in {k} iterations")
    print(f"Tour: ({i}, {j}) Path: {len(tourist.path)}, Cycle: {len(tourist.cycle)}")


def test_every_path(file, shape, n_visits):
    image = io.imread(file, as_gray=True)
    x_size, y_size = 100, 100
    image = transform.resize(image, (x_size, y_size), anti_aliasing=True)
    space = Environment(image, shape)
    # Loop to traverse all the tourist of an image
    m, n = space.data.shape
    for i, j in product(range(m), range(n)):
        point = Point(i, j)
        tourist = Tourist(space, n_visits, point)
        for k in range(m*n):
            tourist.step()
            if tourist.found:
                break
        print(f"{tourist.found} in {k} iterations")
        print(f"Tour: ({i}, {j}) Path: {len(tourist.path)}, Cycle: {len(tourist.cycle)}")


if __name__ == "__main__":
    file = "data/image.png"
    shape = "square"
    n_visits = 3
    test_one_path(file, shape, n_visits)

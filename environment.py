import numpy as np
from collections import namedtuple
Point = namedtuple('Point', 'x y')


def shape_neighborhood(index):
    """
    # # #
    # @ #
    # # #
    """
    # x == 0 and y == 0:
    x0y0 = [(0, 1), (1, 1), (1, 0)]
    # x == 0 and y == ymax - 1:
    x0yM = [(1, 0), (1, -1), (0, -1)]
    # x == xmax - 1 and y == 0:
    xMy0 = [(-1, 0), (-1, 1), (0, 1)]
    # x == xmax - 1 and y == ymax - 1:
    xMyM = [(-1, 0), (0, -1), (-1, -1)]
    # x == 0:
    x0y = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    # x == xmax - 1:
    xMy = [(-1, 0), (-1, 1), (0, 1), (0, -1), (-1, -1)]
    # y == 0:
    xy0 = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)]
    # y == ymax - 1:
    xyM = [(-1, 0), (1, 0), (1, -1), (0, -1), (-1, -1)]
    # x, y
    xy = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    shape = [x0y0, x0yM, xMy0, xMyM, x0y, xMy, xy0, xyM, xy]
    return shape[index]


class Environment:
    def __init__(self, data):
        self.data = data

    def possibles(self, point):
        x, y = point
        value = self.data[x, y]
        region, shape = self.neighbors(point)
        indexes = np.argsort(abs(region - value))
        return indexes, shape

    def neighbors(self, point):
        x, y = point
        xmax, ymax = self.data.shape
        if x == 0 and y == 0:
            idx = 0
            region = np.r_[self.data[x:x+2, y+1], self.data[x+1, y]]
        elif x == 0 and y == ymax - 1:
            idx = 1
            region = np.r_[self.data[x+1, y], self.data[x:x+2, y-1][::-1]]
        elif x == xmax - 1 and y == 0:
            idx = 2
            region = np.r_[self.data[x-1, y], self.data[x-1:x+1, y+1]]
        elif x == xmax - 1 and y == ymax - 1:
            idx = 3
            region = np.r_[self.data[x-1, y], self.data[x-1:x+1, y-1][::-1]]
        elif x == 0:
            idx = 4
            region = np.r_[self.data[x:x+2, y+1], self.data[x+1, y], self.data[x:x+2, y-1][::-1]]
        elif x == xmax - 1:
            idx = 5
            region = np.r_[self.data[x-1, y], self.data[x-1:x+1, y+1], self.data[x-1:x+1, y-1][::-1]]
        elif y == 0:
            idx = 6
            region = np.r_[self.data[x-1, y], self.data[x-1:x+2, y+1], self.data[x+1, y]]
        elif y == ymax - 1:
            idx = 7
            region = np.r_[self.data[x-1, y], self.data[x+1, y], self.data[x-1:x+2, y-1][::-1]]
        else:
            idx = 8
            region = np.r_[self.data[x-1, y], self.data[x-1:x+2, y+1], self.data[x+1, y], self.data[x-1:x+2, y-1][::-1]]
        return np.array(region, dtype=int), shape_neighborhood(idx)


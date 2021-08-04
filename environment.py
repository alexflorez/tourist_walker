import numpy as np


class Environment:
    def __init__(self, data):
        self.data = data.astype(int)

    def possibles(self, point, rule):
        value = self.data[point]
        ixs, jys = self.neighbors_clock(point)
        region = self.data[ixs, jys]
        interest = abs(region - value)
        if rule == "max":
            interest = -interest
        indexes = np.argsort(interest)

        r = ixs[indexes]
        c = jys[indexes]
        return list(zip(r, c))

    def neighbors_clock(self, point):
        """
        8 1 2
        7 @ 3
        6 5 4
        """
        x, y = point
        xmax, ymax = self.data.shape
        if x == 0 and y == 0:
            ixs = (x + 0, x + 1, x + 1)
            jys = (y + 1, y + 1, y + 0)
        elif x == 0 and y == ymax - 1:
            ixs = (x + 1, x + 1, x + 0)
            jys = (y + 0, y - 1, y - 1)
        elif x == xmax - 1 and y == 0:
            ixs = (x - 1, x - 1, x + 0)
            jys = (y + 0, y + 1, y + 1)
        elif x == xmax - 1 and y == ymax - 1:
            ixs = (x - 1, x + 0, x - 1)
            jys = (y + 0, y - 1, y - 1)
        elif x == 0:
            ixs = (x + 0, x + 1, x + 1, x + 1, x + 0)
            jys = (y + 1, y + 1, y + 0, y - 1, y - 1)
        elif x == xmax - 1:
            ixs = (x - 1, x - 1, x + 0, x + 0, x - 1)
            jys = (y + 0, y + 1, y + 1, y - 1, y - 1)
        elif y == 0:
            ixs = (x - 1, x - 1, x + 0, x + 1, x + 1)
            jys = (y + 0, y + 1, y + 1, y + 1, y + 0)
        elif y == ymax - 1:
            ixs = (x - 1, x + 1, x + 1, x + 0, x - 1)
            jys = (y + 0, y + 0, y - 1, y - 1, y - 1)
        else:
            ixs = (x - 1, x - 1, x + 0, x + 1, x + 1, x + 1, x + 0, x - 1)
            jys = (y + 0, y + 1, y + 1, y + 1, y + 0, y - 1, y - 1, y - 1)
        return np.array(ixs), np.array(jys)

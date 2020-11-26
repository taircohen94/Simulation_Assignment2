import copy
import math


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x,self.y

    def get_dist(self, other_pos):

        x = self.x - other_pos.x
        y = self.y - other_pos.y

        return math.pow(x ** 2 + y ** 2, 0.5)

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return copy.deepcopy(self)

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return copy.deepcopy(self)

    def mul_scalar(self, scalar):
        self.x *= scalar
        self.y *= scalar
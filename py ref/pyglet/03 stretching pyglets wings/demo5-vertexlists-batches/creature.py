from math import cos, pi, sin
from random import uniform

class Creature(object):
    "Stores the world-coordinates and shape of a rendered monster"

    def __init__(self, shape, position=None, angle=None):
        self.shape = shape
        if position is None:
            position = (0, 0)
        self.x, self.y = position
        if angle is None:
            angle = uniform(-pi, +pi)
        self.angle = angle
        self.da = 0
        self.velocity = 0

    def update(self, dt):
        self.angle += self.da
        self.x -= self.velocity * cos(self.angle)
        self.y -= self.velocity * sin(self.angle)

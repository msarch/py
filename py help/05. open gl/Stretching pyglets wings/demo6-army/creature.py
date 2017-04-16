from math import cos, pi, sin

class Creature(object):
    "Stores the world-coordinates and shape of a rendered monster"

    def __init__(self, shape, position=None, angle=0):
        self.shape = shape
        if position is None:
            position = (0, 0)
        self.x, self.y = position
        self.angle = angle
        self.da = 0
        self.dx = 0
        self.dy = 0

    def update(self, dt):
        self.angle += self.da
        self.x += self.dx
        self.y -= self.dy


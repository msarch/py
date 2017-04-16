from math import cos, sin
from random import uniform

class Creature(object):
    "Stores the world-coordinates and shape of a rendered monster"

    def __init__(self, shape, position=None, angle=0):
        self.shape = shape
        if position is None:
            position = (0, 0)
        self.x, self.y = position
        self.angle = angle


class Ghost(Creature):
    "A creature that wanders the extent of its room in ghostly torment"

    def __init__(self, shape, position=None, angle=0):
        Creature.__init__(self, shape, position, angle)
        self.room = None
        self.size = 7
        self.speed = uniform(0.1, 1.5)

    def update(self, dt):
        if self.speed > 0:
            goal = self.room.end
        else:
            goal = self.room.start
        dist = \
            (self.x - goal[0]) ** 2 + \
            (self.y - goal[1]) ** 2
        if dist < 0.5:
            self.speed *= -1

        self.x += sin(self.room.angle) * self.speed
        self.y += cos(self.room.angle) * self.speed


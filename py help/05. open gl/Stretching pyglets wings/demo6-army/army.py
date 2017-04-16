from math import cos, pi, sin, sqrt
from random import randint, uniform
from creature import Creature
from shape import Shape


def rand_point(radius):
    dist = sqrt(uniform(0, radius*radius))
    bearing = uniform(-pi, +pi)
    return dist * sin(bearing), dist * cos(bearing)


class Army(Creature):
    """
    An army is just like a single creature, but it has a shape which looks like
    many creatures. Notably, it is still rendered in a single batch.draw() call.
    """

    @staticmethod
    def MakeShape(size, extent, menagerie):
        "make a single shape consisting of many ghosts"
        shapes = []
        for _ in range(size):
            shape = menagerie[randint(0, len(menagerie)-1)]
            shape = shape.offset(*rand_point(extent))
            shape.angle = uniform(-pi, +pi)
            shapes.append(shape)
        return Shape(shapes)


from math import atan, pi, sqrt
from random import randint

from primitive import Primitive
from shape import Shape
from vertexutils import offset, rotate

width = 22
roomColor = (0, 0, 0)

class Room(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.shape = None
        self.angle = self.get_angle()

    def make_shape(self):
        primitive = Primitive(self.make_verts(), roomColor)
        self.shape = Shape([primitive])

    def get_angle(self):
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        if dy == 0:
            if dx > 0:
                angle = +pi/2
            elif dx < 0:
                angle = -pi/2
            else:
                angle = None
        else:
            if dx == 0 and dy < 0:
                angle = pi
            else:
                angle = atan(dx/dy)
                if dy < 0:
                    if dx > 0:
                        angle = pi + angle
                    else:
                        angle = -pi + angle
        return angle

    def make_verts(self):
        # create room geometry with bevelled corners
        root2 = sqrt(2)
        bevelLen = width / (1 + 2 / root2)
        bevelVerts = [
            -width/2, -width/2 + bevelLen / root2,
            -bevelLen/2, -width/2,
            +bevelLen/2, -width/2,
            +width/2, -width/2 + bevelLen / root2,
        ]
        bevelVerts = rotate(bevelVerts, self.angle)
        startVerts = offset(bevelVerts, *self.start)
        endVerts = rotate(bevelVerts, pi)
        endVerts = offset(endVerts, *self.end)

        return [
            startVerts[0], startVerts[1],
            endVerts[6], endVerts[7],
            startVerts[2], startVerts[3],
            endVerts[4], endVerts[5],
            startVerts[4], startVerts[5],
            endVerts[2], endVerts[3],
            startVerts[6], startVerts[7],
            endVerts[0], endVerts[1],
        ]


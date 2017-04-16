from math import pi
from unittest import main, TestCase

from room import Room


class Room_test(TestCase):

    def testAngle(self):
        up = Room((0, 0), (0, 1))
        self.assertEquals(up.angle(), 0, "bad angle up")

        upright = Room((0, 0), (1, 1))
        self.assertEquals(upright.angle(), pi/4, "bad angle upright")

        right = Room((0, 0), (1, 0))
        self.assertEquals(right.angle(), pi/2, "bad angle right")

        upleft = Room((0, 0), (-1, 1))
        self.assertEquals(upleft.angle(), -pi/4, "bad angle upleft")

        down = Room((0, 0), (0, -1))
        self.assertEquals(down.angle(), pi, "bad angle down")

        downleft = Room((0, 0), (-1, -1))
        self.assertEquals(downleft.angle(), -3*pi/4, "bad angle downleft")

        left = Room((0, 0), (-1, 0))
        self.assertEquals(left.angle(), -pi/2, "bad angle left")

        downright = Room((0, 0), (+1, -1))
        self.assertEquals(downright.angle(), +3*pi/4, "bad angle downright")

        degenerate = Room((0, 0), (0, 0))
        self.assertEquals(degenerate.angle(), None, "bad angle degenerate")

if __name__ == '__main__':
    main()

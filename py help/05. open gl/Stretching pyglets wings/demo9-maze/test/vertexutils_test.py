from math import pi
from unittest import main, TestCase

from vertexutils import offset, rotate


class Vertexutils_test(TestCase):

    def testOffset(self):
        verts = [1, 2, 3, 4]
        self.assertEquals(offset(verts, 10, 20), [11, 22, 13, 24], "bad offset")
        self.assertEquals(offset([], 10, 20), [], "bad offset")

    def testRotate(self):
        verts = [1, 2, 3, 4]
        actual = rotate(verts, 0)
        self.assertEquals(actual, verts, "bad rotate 0")
        self.assertEquals(rotate([], 123), [], "bad degenerate rotate 0")

        actual = rotate(verts, pi/2)
        self.assertAlmostEquals(actual[0], 2.0, msg="bad rotate pi 0")
        self.assertAlmostEquals(actual[1], -1.0, msg="bad rotate pi 1")
        self.assertAlmostEquals(actual[2], 4.0, msg="bad rotate pi 2")
        self.assertAlmostEquals(actual[3], -3.0, msg="bad rotate pi 3")

if __name__ == '__main__':
    main()

"""
this example profiles the Polygon object's collidepoly, distance, and raycast methods
"""


import cProfile

from numpy import array
from pylygon import Polygon








def main():

    triangle = Polygon([(0, 70), (110, 0), (110, 70)])
    rhombus = Polygon([(0, 80), (20, 0), (80, 0), (60, 80)])

    triangle.move_ip(200, 200)
    rhombus.move_ip(300, 300)

    r = array([-25, -40])
    # no collision
    for i in xrange(1000):
        triangle.collidepoly(rhombus)
        triangle.distance(rhombus, -r)
        triangle.raycast(rhombus, -r)

    # raycast collision
    r = array([25, 40])
    for i in xrange(1000):
        triangle.collidepoly(rhombus)
        triangle.distance(rhombus, -r)
        triangle.raycast(rhombus, -r)

    # collision
    triangle.move_ip(*r)
    for i in xrange(1000):
        triangle.collidepoly(rhombus)
        triangle.distance(rhombus, -r)
        triangle.raycast(rhombus, -r)



if __name__ == '__main__':
    cProfile.run('main()')


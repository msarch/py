# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------
# vector.py
# http://introcs.cs.princeton.edu/python/33design/vector.py.html
# Introduction to Programming in Python: An Interdisciplinary Approach
# Robert Sedgewick, Princeton University
#
# Spatial vectors
# A spatial vector is an abstract entity that has a magnitude and a direction.
# To specify a vector, it suffices to specify a point in Cartesian coordinates.
# The direction is the ray from the origin to the point and the magnitude is
# the length of the arrow (distance from the origin to the point).
# This concept extends to any number of dimensions: an ordered list of n real
# numbers (the coordinates of an n-dimensional point) suffices to specify
# a vector in n-dimensional space.
#
# API.
#
#   Addition: x + y = (x0 + y0, x1 + y1, ..., xn-1 + yn-1)
#   Scalar product: αx = (αx0, αx1, ..., αxn-1)
#   Dot product: x · y = x0y0 + x1y1 + ... + xn-1yn-1
#   Magnitude: |x| = (x02 + x12 + ... + xn-12)1/2
#   Direction: x / |x| = (x0 / |x|, x1 / |x|, ..., xn-1 / |x|)
#   Those definitions lead to this API:

#Vector API
#As with Complex, this API does not explicitly specify that the data type is
#immutable, but we know that client programmers (who are likely to be thinking
#in terms of the mathematical abstraction) will certainly expect that
#convention, and perhaps we would rather not explain to them that we are trying
#to protect them from aliasing bugs!
#Representation. Our first choice in developing an implementation is to choose
#a representation for the data. Using an array to hold the Cartesian coordinates
#provided in the constructor is a clear choice, but not the only reasonable choice.
#If warranted, the implementation can change the coordinate system without affecting client code.
#Implementation. Given the representation, the code that implements all of these
#operations is straightforward, as you can see in the Vector class defined in
#vector.py. The constructor makes a defensive copy of the client array and none
#of the methods assigns a value to the copy, so that Vector objects are immutable.
#How can we ensure immutability when it seems that the client is free to compose
#code like x[i] = 2.0? The answer to this question lies in a special method that
#we do not implement in an immutable data type: in such a case, Python calls the
#special method __setitem__() instead of __getitem__(). Since Vector does not
#implement that method, such client code would raise an AttributeError at run time.
#-----------------------------------------------------------------------

import math

#-----------------------------------------------------------------------

class Vector(object):

    # Construct a new Vector object with numeric Cartesian coordinates
    # given in array a.
    def __init__(self, a):
        # Make a defensive copy to ensure immutability.
        self._coords = a[:]   # Cartesian coordinates
        self._n = len(a) # Dimension.

    # Return the ith Cartesian coordinate of self.
    def __getitem__(self, i):
        return self._coords[i]

    # Return the sum of self and Vector object other.
    def __add__(self, other):
        result = []
        for i in range(self._n):
            result[i] = self._coords[i] + other._coords[i]
        return Vector(result)

    # Return the difference of self and Vector object other.
    def __sub__(self, other):
        result = []
        for i in range(self._n):
            result[i] = self._coords[i] - other._coords[i]
        return Vector(result)

    # Return the product of self and numeric object alpha.
    def scale(self, alpha):
        result = []
        for i in range(self._n):
            result[i] = alpha * self._coords[i]
        return Vector(result)

    # Return the dot product of self and Vector object other.
    # U . V = U1V1 + U2V2 + U3V3
    # U . V is a number; if U and V are normalised, arccos(U.V) is UV angle

    def dot(self, other):
        result = 0
        for i in range(self._n):
            result += self._coords[i] * other._coords[i]
        return result

    # Return the cross product of self and Vector object other.
    # U x V  = (U2V3 - U3V2, U3V1 - U1V3, U1V2 - U2V1)
    # U x V is a vector, U x V is normal to the plane defined by U and V
    def cross(self, other):
        result = [0,0,0]
        if self._n == 3:
            result[0]= self._coords[1]*other._coords[2] - self._coords[2]*other._coords[1]
            result[1]= self._coords[2]*other._coords[0] - self._coords[0]*other._coords[2]
            result[2]= self._coords[0]*other._coords[1] - self._coords[1]*other._coords[0]
        else:
            result=[]
        return result




    # Return the magnitude, that is, the Euclidean norm, of self.
    def __abs__(self):
        return math.sqrt(self.dot(self))

    # Return the unit vector of self.
    def direction(self):
        return self.scale(1.0 / abs(self))

    # Return a string representation of self.
    def __str__(self):
        return str(self._coords)

    # Return the dimension of self.
    def __len__(self):
        return self._n


class Spherical(Vector):
    """ Construct a new (cartesian coords) Vector from polar: a=(r,φ,θ) coords.
    r is radius, phi azimuth(degrees), theta elevation (degrees)
    """
    #
    #            Z
    #            |
    #            |    . a(r,φ,θ)
    #            |-θ-/:
    #            |  / :
    #            | /  :
    #            |/   :
    #            +----:-------Y
    #           / \   :
    #          /   \  :
    #         /--φ--\ :
    #        /       \:
    #       /         .
    #      /
    #     X
    #
    #  a=(a1,a2,a3) with: a1=rcosφsinθ, a2=rsinφsinθ, a3=rcosθ

    def __init__(self, a):
        # Call Vector with converted coordinates
        i= a[0] * cos_d(a[1]) * sin_d(a[2])
        j= a[0] * sin_d(a[1]) * sin_d(a[2])
        k= a[0] * cos_d(a[2])
        super(Spherical, self).__init__([i,j,k])

#-----------------------------------------------------------------------
def sin_d(deg):
    """ Return sin with handling of multiples of 90 for perfect right angles
    """
    deg = deg % 360
    if deg == 90:
        return 1.0
    elif deg == 180:
        return 0
    elif deg == 270:
        return -1.0
    rad = math.radians(deg)
    return math.sin(rad)

def cos_d(deg):
    """ Return cos with handling of multiples of 90 for perfect right angles
    """
    deg = deg % 360
    if deg == 90:
        return 0
    elif deg == 180:
        return -1.0
    elif deg == 270:
        return 0
    rad = math.radians(deg)
    return math.cos(rad)
# For testing.
# Create and use some Vector objects.

def main():

    xCoords = [1.0, 2.0, 3.0, 4.0]
    yCoords = [5.0, 2.0, 4.0, 1.0]

    x = Vector(xCoords)
    y = Vector(yCoords)

    print('x        = ' + str(x))
    print('y        = ' + str(y))
    print('x + y    = ' + str(x + y))
    print('10x      = ' + str(x.scale(10.0)))
    print('|x|      = ' + str(abs(x)))
    print('<x, y>   = ' + str(x.dot(y)))
    print('|x - y|  = ' + str(abs(x - y)))

if __name__ == '__main__':
    main()

#-----------------------------------------------------------------------

# python vector.py
# x        = [1.0, 2.0, 3.0, 4.0]
# y        = [5.0, 2.0, 4.0, 1.0]
# x + y    = [6.0, 4.0, 7.0, 5.0]
# 10x      = [10.0, 20.0, 30.0, 40.0]
# |x|      = 5.477225575051661
# <x, y>   = 25.0
# |x - y|  = 5.0990195135927845


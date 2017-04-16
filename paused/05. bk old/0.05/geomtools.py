



# Rev : 0.2


from math import degrees, atan2
from math import sqrt, pow
from math import radians, sin, cos
import math



#         BASIC FUNCTIONS
#--------------------------------------


def angle(x0, y0, x1, y1):
    return degrees( atan2(y1-y0, x1-x0) )

def distance(x0, y0, x1, y1):
    return sqrt(pow(x1-x0, 2) + pow(y1-y0, 2))

def coordinates(x0, y0, distance, angle):
    x1 = x0 + cos(radians(angle)) * distance
    y1 = y0 + sin(radians(angle)) * distance
    return x1, y1

def cos_sin_deg(deg):
    """Return the cosine and sin for the given angle
    in degrees, with special-case handling of multiples
    of 90 for perfect right angles
    """
    deg = deg % 360.0
    if deg == 90.0:
        return 0.0, 1.0
    elif deg == 180.0:
        return -1.0, 0
    elif deg == 270.0:
        return 0, -1.0
    rad = math.radians(deg)
    return math.cos(rad), math.sin(rad)

# --> from nodebox.geometry
#def rotate(x, y, x0, y0, angle):
#    """ Returns the coordinates of (x,y) rotated around origin (x0,y0).
#    """
#    x, y = x-x0, y-y0
#    a, b = cos(radians(angle)), sin(radians(angle))
#    return (x*a-y*b+x0, y*a+x*b+y0)
    




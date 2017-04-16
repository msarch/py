#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : t(ime),o,x,y : tools for movement on a 2d plane
# ref :
#        'planar'
#        'nodeboxGL' : voir geometry.py et __init__ (tout bon pour implementation path, couleur, etc..)
#        'matrix' from kai chang (http://www.syntagmatic.net)

# r0.3



from math import degrees, atan2
from math import sqrt, pow
from math import radians, sin, cos
import math



#         GENERAL FUNCTIONS
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
    """ Return the cosine and sin for the given angle
    in degrees, with special-case handling of multiples
    of 90 for perfect right angles
    """
    deg = deg % 360
    if deg == 90:
        return 0, 1.0
    elif deg == 180:
        return -1.0, 0
    elif deg == 270:
        return 0, -1.0
    rad = math.radians(deg)
    return math.cos(rad), math.sin(rad)

#  SIMPLE AFFINE TRANSFORMATION MATRIX
#--------------------------------------
#        [a b c]
#        [d e f]
#        [g h i]
# will be represented as a list of nine elements :
# matrix = [a, b, c, d, e, f, g, h, i]

def id_matrix():
    """ Returns the 3x3 identity matrix
    """ 
    return([1, 0, 0, 0, 1, 0, 0, 0, 1])

def show(m):
    """ Print out matrix
    """
    print '[', m[0], m[1], m[2] ,']'
    print '[', m[3], m[4], m[5] ,']'
    print '[', m[6], m[7], m[8] ,']'
    
def mmult(m,M):
    """3x3 matrix multiplication : returns a 3x3 matrix.
    """
    # matrix multiplication : 
    #    [a b c]   [A B C]   [aA+bD+cG  aB+bE+cH  aC+bF+cI]
    #    [d e f] * [D E F] = [dA+eD+fG  dB+eE+fH  dC+eF+fI]
    #    [g h i]   [G H I]   [gA+hD+iG  gB+hE+iH  gC+hF+iI]
    #
    return [m[0]*M[0] + m[1]*M[3] + m[2]*M[6],
        m[0]*M[1] + m[1]*M[4] + m[2]*M[7],
        m[0]*M[2] + m[1]*M[5] + m[2]*M[8],
        m[3]*M[0] + m[4]*M[3] + m[5]*M[6],
        m[3]*M[1] + m[4]*M[4] + m[5]*M[7],
        m[3]*M[2] + m[4]*M[5] + m[5]*M[8],
        m[6]*M[0] + m[7]*M[3] + m[8]*M[6],
        m[6]*M[1] + m[7]*M[4] + m[8]*M[7],
        m[6]*M[2] + m[7]*M[5] + m[8]*M[8]
    ]

def vmult(x,y,m):
    """ vector (x,y,1) by 3x3 matrix multiplication : returns (x'(int), y'(int))
    """
    #    [x']   [m0 m1 m2]   [x]
    #    [y'] = [m3 m4 m5] * [y]
    #    [z']   [m6 m7 m8]   [1]
    # z and z' always set to 1 because
    # m is always a 2d affine transformation matrix

    return (int(m[0]*x+m[1]*y+m[2]), int(m[3]*x+m[4]*y+m[5]))


def copy(m1):
    pass

def translation_matrix(dx, dy):
    """ Returns the transformation matrix for a (dx,dy) translation.
    """ 
    return ([1, 0, dx, 0, 1, dy, 0, 0 ,1])

def speed_heading_matrix(speed, heading):
    """ Returns the 3x3 transformation matrix for a translation :
        during dt at speed = speed, heading = heading
    """
    c,s = cos_sin_deg(heading)
    return ([1, 0, speed*c, 0, 1, speed*s, 0, 0 ,1])
        
                
def scale_matrix(sx,sy):
    """ scale matrix, scale factors=(sx,sy), origin=(0,0)
    """ 
    return([sx, 0, 0, 0, sy, 0, 0, 0, 1])

def rotation_matrix(alpha):
    """ rotation matrix, center=(0,0), angle=alpha(degrees)
    """ 
    c,s= cos_sin_deg(alpha)
    return([c, -s, 0, s, c, 0, 0, 0, 1])

def avelo_rotation_matrix(omega):
    """ rotation matrix, center=object's centroid ??????????
        (0,0), angle : alpha (degres)
    """ 
    pass

def x_sym_matrix():
    """ transformation matrix for the symmetry through x axis
    """ 
    return([1, 0, 0, 0, -1, 0, 0, 0, 1])

def y_sym_matrix():
    """ transformation matrix for the symmetry through y axis
    """ 
    return([-1, 0, 0, 0, 1, 0, 0, 0, 1])

im = id_matrix
tm = translation_matrix
sm = scale_matrix
rm = rotation_matrix
xsm = x_sym_matrix
ysm = y_sym_matrix

#   COMPOSITE TRANSFORMATION MATRIX
#--------------------------------------

def general_symetry_matrix(x,y,alpha):
    """ Returns the 3x3 transformation matrix for a symmetry operation
        through an axis defined by a point (x,y) and an angle (alpha)
    """ 
    m1=tm(x,y)
    m2=rm(alpha)
    m3=y_sym_matrix()
    m4=tm(-x,-y)
    m5=rm(-alpha)
 
    return (mmult(m5,mmult(m4,mmult(m3,(mmult(m1,m2))))))

gsm = general_symetry_matrix


#         TIME RELATED FUNCTIONS
#--------------------------------------

def lin (dt,a,b):
    u=(a*dt)+b
    return u

#def check_frontier(box,frontier):
#    
#    return(touch)   
#    return(in)
#    return(out)
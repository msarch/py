#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * july 2014 * bw-rev104
'''

#--- IMPORTS ------------------------------------------------------------------
from pyglet.gl import GL_TRIANGLE_STRIP, glPushMatrix, glTranslatef,\
    glRotatef, glPopMatrix
from . colors import Color
from . shapes import Primitive

#--- USERS PRIMITIVES ---------------------------------------------------------
class Kapla(Primitive):
    """ horizontal kapla sized rectangle, origin @ lower left corner
    """
    def __init__(self,color=Color.white):
        verts=[(0,0),(11,0),(0,33),(11,33)]
        Primitive.__init__ (self,verts,color, GL_TRIANGLE_STRIP)

class Ghost(Primitive):
    def __init__(self,color=Color.white):
        contour = [
        (-7, -7),   # 0
        (-7.0, 0.0),# 1
        (-5, -5),   # 22
        (-6.7, 2.0),# 2
        (-3, -7),   # 21
        (-5.9, 3.8),# 3
        (-1, -7),   # 20
        (-4.6, 5.3),# 4
        (-1, -5),   # 19
        (-2.9, 6.4),# 5
        (1, -5),    # 18
        (-1.0, 6.9),# 6
        (3, -7),    # 16
        (1.0, 6.9), # 7
        (5, -5),    # 15
        (2.9, 6.4), # 8
        (7, -7),    # 14
        (4.6, 5.3), # 9
        (7.0, 0.0), # 13
        (4.6, 5.3), # 10
        (6.7, 2.0), # 12
        (5.9, 3.8), # 11
        ]
        Primitive.__init__ (self,contour,color, GL_TRIANGLE_STRIP)

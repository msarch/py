#!/usr/local/bin/python2.7
# encoding: utf-8

'''
Circle, outline only : GL_LINE_STRIP
vertices are ordered clockwise : 12, 1, 2, 3, 4, 5...
number of vertices per half-circle for a smooth result is : radius/5 +3
'''

#--- IMPORTS ------------------------------------------------------------------
from math import pi, sin, cos
from engine import *

##--- CONSTANTS AND VARIABLES -------------------------------------------------
radius=100
stepangle = pi/(int(radius/5)+3)
phi=0
verts=[]

#--- VERTEX GENERATION --------------------------------------------------------
verts.append((0, radius))
while phi<pi:
    x = radius * sin(phi)
    y = radius * cos(phi)
    verts.append((x, y))
    phi += stepangle
verts.append((0,-radius))  # add right side vertex
for vert in reversed(verts):
    verts.append((-vert[0],vert[1]))


#--- SHAPE DECLARATION --------------------------------------------------------
Shape(id='circle1', primtype = 'GL_LINE_STRIP', verts=verts)


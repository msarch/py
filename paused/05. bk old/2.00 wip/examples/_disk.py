#!/usr/local/bin/python2.7
# encoding: utf-8

'''
Circle, plain color : TRIANGLE_STRIP
vertices are ordered  : 11, 12, 10, 1, 9, 2, 8, 3, 7, 4, 6, 5...
number of vertices per half-circle for a smooth result is : radius/5 +3
'''

#--- IMPORTS ------------------------------------------------------------------
from math import pi, sin, cos
from engine.shape import Shape

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
    verts.append((x, -y))
    phi += stepangle
verts.append((0,-radius))  # add right side vertex
for v in reversed(verts):
    verts.append((-v[0],v[1]))

Shape(id='disk1', primtype = 'GL_TRIANGLE_STRIP', vertices=verts)

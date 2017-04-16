#!/usr/local/bin/python2.7
# encoding: utf-8

'''
Centered Rectangle, Origin @ centroid w=width, h=height, color=color
2--------3
|   .x   |
0--------1
'''

#--- IMPORTS ------------------------------------------------------------------
from bw import *

##--- CONSTANTS AND VARIABLES -------------------------------------------------
w = 100
h = 50

#--- VERTEX GENERATION --------------------------------------------------------
verts = [(-w/2, -h/2),(w/2, -h/2), (-w/2, h/2),(w/2, h/2)]

#--- SHAPE DECLARATION --------------------------------------------------------
Shape(id='rec1', primtype = GL_TRIANGLE_STRIP, verts=verts, visible=True)


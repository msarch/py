#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Author:  msarch@free.fr
# Purpose: draws a square room from a list of measurements
# Created:   .  .2012
# License: MIT License
#
# draws a sphere with dots, u and v's to be defined
# rotates ONCE the sphere around Z axis

# Add the upper directory (where the nodebox module is) to the search path.
import os, sys; sys.path.insert(0, os.path.join(".."))

from nodebox.graphics import *
from math import sin, cos

# Define parametric equations for each axis.
# Although we define an z coordinate,
# it is only used in transformations and shading;
# it is not used in the drawing
# (although it could be if you wanted to add perspective).

r = 240
umax=9 # number of parallels (lignes)
vmax=8 # number of meridians (colonnes)
theta =5

dotx = []
doty = []
dotz = []

# latitude, longitude to cartesian coords
def tocartx(u,v): return r * sin(u) * cos(v)
def tocarty(u,v): return r * sin(u) * sin(v)
def tocartz(u,v): return r * cos(u)

# u and v to latitude and longitude angles (rad)
def tolatitude(x): return 1.0 * x / umax * pi * 0.5
def tolongitude(x): return 1.0 * x / vmax * pi * 2

# apply a move, here a single rotation around the z axis only
def xmoved(x,y,z): return (x * cos(theta)) - (y * sin (theta))
def ymoved(x,y,z): return (x * sin(theta)) + (y * cos(theta))
def zmoved(x,y,z): return z

# initialize a  'pseudo arrays' (nested list in fact)
# with the x,y,z cartesian coords of points at sphere's u,v's.
for u in xrange(umax):
    dotx.append([])
    doty.append([])
    dotz.append([])
    for v in xrange(vmax):
            lat = tolatitude(u)
            lon = tolongitude(v)
            # Get points 3D coords.

            x0=tocartx(lat,lon)
            y0=tocarty(lat,lon)
            z0=tocartz(lat,lon)

            x1= xmoved(x0,y0,z0)
            y1= ymoved(x0,y0,z0)
            z1= zmoved(x0,y0,z0)

            dotx[u].append(x1)
            doty[u].append(y1)
            dotz[u].append(z1)

            # Transform/Project points 3D coords to 2D canvas coord.
            #projx[i][j] = dotx[i][j]
            #projy[i][j] = doty[i][j]

def draw(canvas):

    # The trick is not to clear the canvas each frame.
    # Instead, we only draw a background in the first frame,
    # and then gradually build up the composition with the next points each frame.
    if canvas.frame == 1:
        background(1)

    # Translate the canvas origin point to the center.
    # The attractor can yield negative (x,y)-values,
    # so if we leave the origin point in the bottom left,
    # part of the pattern will fall outside the drawing area.
    translate(canvas.width/2, canvas.height/2)

    # Note how the fill color has a very low alpha (i.e. high transparency).
    # This makes the pattern more fine-grained,
    # as many transparent points will need to overlap to form a thicker line.
    fill(0, 0.1)

    # Go through the array and draw rectangles.
    #
    #  |(Y)
    #  |
    #  |
    #  0------(X)
    #

    for i in xrange(umax):
        for j in xrange(vmax):
            # Draw a pixel at the current x and y coordinates.
            rect(dotx[i][j],doty[i][j],2,2)

canvas.size = 700, 700
canvas.run(draw)



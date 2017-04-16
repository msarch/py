#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# draws a sphere with dots, u and v's to be defined
# rotates the sphere around Z axis

# Add the upper directory (where the nodebox module is) to the search path.
import os, sys; sys.path.insert(0, os.path.join(".."))

from nodebox.graphics import *
from math import sin, cos


r = 240
umax=15 # number of parallels (lignes)
vmax=15 # number of meridians (colonnes)
theta =0.2

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

            x=tocartx(lat,lon)
            y=tocarty(lat,lon)
            z=tocartz(lat,lon)

            dotx[u].append(x)
            doty[u].append(y)
            dotz[u].append(z)


            # Transform/Project points 3D coords to 2D canvas coord.
            #projx[i][j] = dotx[i][j]
            #projy[i][j] = doty[i][j]

def draw(canvas):
    canvas.clear()
    stroke(0, 0.2)
    # Translate the canvas origin point to the center.
    translate(canvas.width/2, canvas.height/2)

    # Note how the fill color has a very low alpha (i.e. high transparency).
    # This makes the pattern more fine-grained,
    # as many transparent points will need to overlap to form a thicker line.
    # fill(0, 0.1)

    # Go through the array and draw dots as small rectangles.
    #
    #  |(Y)
    #  |
    #  |
    #  0------(X)
    #

    for i in xrange(umax):
        for j in xrange(vmax):

            x= xmoved(dotx[i][j],doty[i][j],dotz[i][j])
            y= ymoved(dotx[i][j],doty[i][j],dotz[i][j])
            z= zmoved(dotx[i][j],doty[i][j],dotz[i][j])

            dotx[i][j]= x
            doty[i][j]= y
            dotz[i][j]= z

            # Draw a pixel at the current x and y coordinates.
            rect(dotx[i][j],doty[i][j],2,2)

canvas.size = 700, 700
canvas.run(draw)



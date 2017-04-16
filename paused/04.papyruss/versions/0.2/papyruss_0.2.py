#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Add the upper directory (where the nodebox module is) to the search path.
import os, sys;sys.path.insert(0,os.path.join("..",".."))

from nodebox.graphics import *
import squirtle
import amethyst

# TODO : load/read svg, extract paths to nodebox paths to be able to modify them
# TODO :  possible re-export screens to svg (svg write) ?

White= color(amethyst.color("white"))
path1 = BezierPath()
path1.moveto(0,0)
path1.curveto(0,16.585,28.321,28.335,28.321,28.335)

filename = "svg/curve.svg"
s = squirtle.SVG(filename)

def draw(canvas):

    background(color(amethyst.color("red")))
    drawpath(path1, fill=None, stroke=White)
    s.draw(200, 200, scale=1, angle=0)

canvas.fps = 60
canvas.size = 600, 400
# canvas.fullscreen = True
canvas.run(draw)

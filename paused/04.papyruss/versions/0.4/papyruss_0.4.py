#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Add the upper directory to the search path.
# in case the nodebox module is there.
import os, sys;sys.path.insert(0,os.path.join("..",".."))

from nodebox.graphics import canvas, drawpath, triangle
from nodebox.graphics import fill, stroke, background, strokewidth
from nodebox.graphics import translate, scale, rotate

from random import random
import TT.palette as palette              # dictionnaire de couleurs (mod:TT)
import TT.svg as svg                      # parser svg de Nodebox (mod:TT pour l'adapter à Nodebox GL)

White = palette.tint("white")
Red = palette.tint("red")

# The parse() command will return a list
# containing the shapes in the SVG file.
paths = svg.parse(open("svg/leaf2.svg").read())

def draw(canvas):
    background(Red)
    xc=canvas.width/2
    yc=canvas.height/2
    stroke(White) # 75% transparent black.
    strokewidth(1)
    triangle(xc, yc, xc+50, yc+100, xc+100, yc)

# While rect() and ellipse() expect x, y, width, height parameters,
    # triangle() expects the coordinates of three points,
    # which are connected into a triangle.

    # Clear the current stroke,
    # otherwise it is still active in the next frame
    # when we start drawing the rectangle and the ellipse.
    # nostroke()
   
    # You can also pass Color objects to fill() and stroke().
    # A Color object can be created with the color command.
    # It has clr.r, clr.g, clr.b, clr.a properties :
    #   clr = color(0.25, 0.15, 0.75, 0.5) # 50% transparent purple/blue.
    #   fill(clr)

    for i in range(10):
        dx=random()*200.0
        dy=random()*200.0
        xs=random()*1.6
        ys=random()*1.6
        dr=random()*360.0
        translate(dx,dy)
        scale(xs,ys,1)
        rotate(dr)
        fill(1, 1, 0.9, 0.1)

        for path in paths:
            # Use copies of the paths
            # that adhere to the transformations
            # (translate, scale, rotate) we defined.
            drawpath(path)

canvas.fps = 6
canvas.size = 600, 400
# canvas.fullscreen = True
canvas.run(draw)



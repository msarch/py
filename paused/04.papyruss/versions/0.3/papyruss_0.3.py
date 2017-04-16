#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Add the upper directory (where the nodebox module is) to the search path.
import os, sys;sys.path.insert(0,os.path.join("..",".."))

from nodebox.graphics import canvas, BezierPath, drawpath, triangle, ellipse
from nodebox.graphics import drawpath, color, fill, stroke, nostroke, background, strokewidth
from nodebox.graphics import translate, scale, rotate
from random import random
import squirtle
import amethyst
import amethsvg_MOD01 as svgRead
# couleur dans la librairy 'amethyst'
White= color(amethyst.triplet("white"))

# standard nodeboxGL graphics command
path1 = BezierPath()
path1.moveto(0,0)
path1.curveto(0,16.585,28.321,28.335,28.321,28.335)

# squirtle svg parser
filename = "svg/curve.svg"
path2 = squirtle.SVG(filename)

# svg lib from Nodebox
# The parse() command will return
# a list of the shapes in the SVG file.
paths3 = svgRead.parse(open("svg/curve.svg").read())


def draw(canvas):
    #background(color(amethyst.triplet("red")))

    stroke(0.0, 0.25) # 75% transparent black.
    strokewidth(1)
    triangle(200, 200, 250, 300, 300, 200)

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

    # path2.draw(200, 200, scale=1, angle=0)

    for i in range(10):
        dx=random()*200.0
        dy=random()*200.0
        ds=random()*1.6
        dr=random()*360.0
        translate(dx,dy)
        scale(ds)
        rotate(dr)
        fill(1, 1, 0.9, 0.1)

        for path in paths3:
            # Use copies of the paths
            # that adhere to the transformations
            # (translate, scale, rotate) we defined.
            drawpath(path)




canvas.fps = 60
canvas.size = 600, 400
# canvas.fullscreen = True
canvas.run(draw)



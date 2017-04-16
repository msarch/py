#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# tweak from Nodebox.spikesFilter

import os, sys;sys.path.insert(0,os.path.join("..",".."))

from nodebox.graphics import canvas, drawpath, triangle, endpath
from nodebox.graphics import nofill, stroke, background, strokewidth
from nodebox.graphics import beginpath, moveto, curveto
from nodebox.graphics import Point as Point

from random import random
import TT.palette as palette           # dictionnaire de couleurs (mod:TT)
import TT.svg as svg                      # parser svg de Nodebox (mod:TT)
from TT.geom import distance, angle, coordinates



MOVETO="M"
m = 5   # spike length
c = 0.8 # spike curvature

White= palette.tint("white")
Red= palette.tint("red")

paths = svg.parse(open("svg/leaf2.svg").read())

# The "spike" function between two points.

def perpendicular_curve(pt0, pt1, curvature=0.8):

    d = distance(pt0.x, pt0.y, pt1.x, pt1.y)
    a = angle(pt0.x, pt0.y, pt1.x, pt1.y)

    mid = Point(
        pt0.x + (pt1.x-pt0.x) * 0.5,
        pt0.y + (pt1.y-pt0.y) * 0.5
    )
    dx, dy = coordinates(mid.x, mid.y, m, a-90)

    vx = pt0.x + (mid.x-pt0.x) * curvature
    vy = pt0.y + (mid.y-pt0.y) * curvature
    curveto(vx, vy, dx, dy, dx, dy)

    vx = pt1.x + (mid.x-pt1.x) * curvature
    vy = pt1.y + (mid.y-pt1.y) * curvature
    curveto(dx, dy, vx, vy, pt1.x, pt1.y)


def draw(canvas):
    background(Red)
    xc=canvas.width/2
    yc=canvas.height/2
    stroke(0.0, 0.25) # 75% transparent black.
    strokewidth(1)
    triangle(xc, yc, xc+50, yc+100, xc+100, yc)

    for path in paths:
        prev = None
        for point in path:
            pt=point
            nofill()
            stroke(1)
            strokewidth(0.75)

            if not prev:
                beginpath(pt.x, pt.y)
            elif pt.cmd == MOVETO:
                moveto(pt.x, pt.y)
            else:
                perpendicular_curve(prev, pt, c)

            prev = pt
        endpath()
        drawpath(path)

canvas.fps = 6
canvas.size = 600, 400
# canvas.fullscreen = True
canvas.run(draw)

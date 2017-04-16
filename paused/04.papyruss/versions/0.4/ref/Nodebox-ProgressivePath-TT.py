#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# TT

import os, sys;sys.path.insert(0,os.path.join("..",".."))

import TT.svg
import nodebox.graphics
from nodebox.graphics import path
import os, sys;sys.path.insert(0,os.path.join("..",".."))

from nodebox.graphics import canvas, drawpath, triangle, line, autoclosepath, beginpath, nofill
from nodebox.graphics import stroke, background, strokewidth, endpath, lineto

from random import random
from TT.palette import tint           # dictionnaire de couleurs (mod:TT)
import TT.svg                            # parser svg de Nodebox (mod:TT)

w=10.0
n = 0
points=[]

paths = TT.svg.parse(open("./svg/2ptCurve.svg").read())
path =paths[0]
# print path
for point in path.points(50):
    points.append(point)

def draw(canvas):
   
    xc=canvas.width/2
    yc=canvas.height/2
    nofill()
    stroke(0.0, 0.25) # 75% transparent black.
    strokewidth(5)
    autoclosepath(close=False)
    triangle(xc, yc, xc+50, yc+100, xc+100, yc)
    line(xc, yc, xc+5, yc+234)
    
    global n,w, points
    
    strokewidth(w)
    line(points[n-1].x, points[n-1].y,points[n].x, points[n].y)

    if n<49:
        # print n, w, points[n].x, points[n].y
        w -= 0.2
        n += 1
    else:canvas.stop()


canvas.fps = 6
canvas.size = 600, 400
background = tint("red")
# canvas.fullscreen = True
canvas.run(draw)
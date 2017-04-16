#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Author:  tintouen@gmail.com
# Purpose: draws rectangles, nonstop
# Created:   .  .2013
# License: MIT License

# Rev : 0.1

#--------------------------------------
#              imports
#--------------------------------------

import os, sys;sys.path.insert(0,os.path.join("..",".."))
    # Add the upper directory to the search path.
    # in case the nodebox module is there.
from nodebox.graphics import canvas, rect
from nodebox.graphics import color, fill, stroke, background, strokewidth
from nodebox.graphics import translate, rotate

from random import random

import TT.palette as palette
    # dictionnaire de couleurs (mod:TT)

#--------------------------------------
#             constants
#--------------------------------------

White = palette.tint("white")
Red = palette.tint("red")

canvas.fps = 6
canvas.size = 600, 400

background(Red)

x0=canvas.width/2
y0=canvas.height/2

rectWidth=100
rectHeight=30

#--------------------------------------
#   internal functions & classes
#--------------------------------------

#         function : draw
#--------------------------------------
def draw(canvas):
    """ {{{ 
    - dessine en boucle 
    - Args : canvas (string)
    - Returns : none
    """ 

    stroke(White) # 75% transparent black.
    strokewidth(1)

    # random position, rect rotation, color and tranparency
    x1 = random()*canvas.width
    y1 = random()*canvas.height
        #
        #  | Y
        #  | 
        #  |
        #  |            X
        #  0 ------------
        #

    rot = int(random()*4)*90
    rndColor = color(random(),random(),random(),random())
        # You pass Color objects to fill() and stroke().
        # A Color object can be created with the color command.
        # It has clr.r, clr.g, clr.b, clr.a properties :
        #   clr = color(0.25, 0.15, 0.75, 0.5) # 50% transparent purple/blue.
        #   fill(clr)
        
    translate(x1,y1)
    rotate(rot)
    fill(rndColor)
    rect(0,0,rectWidth,rectHeight)
        # rect() and ellipse() expect x, y, width, height parameters,
        # triangle() expects the coordinates of three points


#--------------------------------------
#                main
#--------------------------------------

canvas.fullscreen = True
canvas.run(draw)



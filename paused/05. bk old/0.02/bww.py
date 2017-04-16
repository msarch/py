#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Author:  tintouen@gmail.com
# Purpose: draws rectangles, nonstop
# Created:   .  .2013
# License: MIT License

# Rev : 0.2

#--------------------------------------
#              comments
#--------------------------------------
# - Rev 0.1 : simples rectangles
# - Rev 0.2 : classes et layers (v. nodebox exemples, 01-drag.py)
#
#  | Y
#  | 
#  |
#  |            X
#  0 ------------
#
#--------------------------------------
#              imports
#--------------------------------------

import os, sys;sys.path.insert(0,os.path.join("..",".."))
    # Add the upper directory to the search path.
    # in case the nodebox module is there.
from nodebox.graphics import canvas, rect
from nodebox.graphics import color, fill, stroke, background, strokewidth
from nodebox.graphics import translate, rotate

from nodebox.graphics import *

from random import random

import TT.palette as palette
    # dictionnaire de couleurs (mod:TT)
    
import csv

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

rect_list = []

#--------------------------------------
#   internal functions & classes
#--------------------------------------

#         Class : DraggableRect
#--------------------------------------
# In the previous examples, drawing occurs directly to the canvas.
# It is also possible to draw into different layers, 
# and then transform / animate the layers individually.
# The Layer class introduces a lot of useful functionality:
# - layers can receive events from the mouse,
# - layers have an origin point (e.g. "center") from which transformations originate,
# - layers have methods such as Layer.rotate() and Layer.scale(),
# - layers can enable motion tweening (i.e. smooth, automatic transititions).

# A Layer has its personal Layer.draw() method that contains drawing commands.
# In this example, we create a subclass of Layer to display a colored, draggable rectangle:
class DraggableRect(Layer):
    
    def __init__(self, *args, **kwargs):
        # A Layer with an extra "clr" property.
        Layer.__init__(self, *args, **kwargs)
        self.clr = Color(0, 0.75)
    
    def draw(self):
        rect(0, 0, self.width, self.height, fill=self.clr, stroke=self.clr)
    
    def on_mouse_enter(self, mouse):
        # When the mouse hovers over the rectangle, highlight it.
        mouse.cursor = HAND
        self.clr.a = 0.75
    
    def on_mouse_leave(self, mouse):
        # Reset the mouse cursor when the mouse exits the rectangle.
        mouse.cursor = DEFAULT
        self.clr.a = 0.5
    
    def on_mouse_drag(self, mouse):
        # When the rectangle is dragged, transform it.
        # Its scale increases as the mouse is moved up.
        # Its angle increases as the mouse is moved left or right.
        self.translate(mouse.dx,mouse.dy)
 

#         function : read csv
#--------------------------------------

def readRectangles():
    

    with open('test.csv') as f:
        r = csv.reader(f)         
        for index, item in enumerate(r):
            print index, item
            
            rect_list.append(item)
            # rect_list is a list of columns : a list of lists 
            # We can of course extract a precise entry of a row with the index.
        del rect_list[0]
            # la premiere ligne du fichier csv ne contient pas de data utile


#         function : draw
#--------------------------------------

def draw(canvas):

    canvas.clear()
    
    # dessin des rectangles du fond
    for item in rect_list:
        clr=color(float(item[4]),float(item[5]),float(item[6]),float(item[7]))
        stroke(clr)
        fill(clr)
        rect(int(item[0]),int(item[1]),int(item[2]),int(item[3]))
            # rect() and ellipse() expect x, y, width, height parameters,
            # triangle() expects the coordinates of three points

    # les calques seront ajoutés automatiquement

   
        
#--------------------------------------
#                main
#--------------------------------------

readRectangles()

r1 = DraggableRect(x=200, y=200, width=200, height=200, origin=(0.5,0.5), name="blue1")
r1.clr = color(0.0, 0.5, 0.75, 0.5)
    # The layer's origin defines the origin point for the layer's placement,
    # its rotation and scale. If it is (0.5, 0.5), this means the layer will transform
    # from its center (i.e. 50% width and 50% height). If you supply integers,
    # the values will be interpreted as an absolute offset from the layer's bottom-left corner.
    # Note:
    # if you have layers that do not need to receive events,
    # set Layer.enabled = False; this saves some time doing expensive matrix operations.

canvas.append(r1)
    # The canvas is essentially a list of layers, just as an image in Photoshop is a list of layers.
    # Appending a layer to the canvas ensures that it gets drawn each frame,
    # that it receives mouse and keyboard events, and that its motion tweening is updated.

# canvas.fullscreen = True
canvas.run(draw)



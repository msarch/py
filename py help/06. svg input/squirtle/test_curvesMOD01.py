
import os, sys; sys.path.insert(0, os.path.join(".."))

from nodebox.graphics import *

import pyglet
from pyglet.gl import *

import sys

import squirtle

filename = "svgs/zapf.svgz"





def draw(canvas):
    canvas.clear()
    nofill()
    stroke(0, 0.25)
    strokewidth(1)
    rect( 50, 50, 50, 50)
    rect(110, 50, 50, 50, stroke=Color(0), strokestyle=DASHED)
    rect(170, 50, 50, 50)


    glClearColor(1,1,1,1)

    squirtle.setup_gl()

    s = squirtle.SVG(filename)
    s.anchor_x, s.anchor_y = s.width/2, s.height/2

    zoom = 1
    angle = 0
    draw_x = 400
    draw_y = 300

    s.draw(draw_x, draw_y, scale=zoom, angle=angle)

canvas.size = 500, 500
canvas.run(draw)


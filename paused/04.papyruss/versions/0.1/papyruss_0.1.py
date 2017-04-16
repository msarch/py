# Add the upper directory (where the nodebox module is) to the search path.
import os, sys;sys.path.insert(0,os.path.join("..",".."))

from nodebox.graphics import *



from random import seed
from math   import sin

import squirtle


filename = "svg/leaf2.svg"
filename2 = "svg/slice 3.svg"
lines = []
s = squirtle.SVG(filename)
s2 = squirtle.SVG(filename2)
# attention squirtle ne lit pas les svg (issus de skertch) dont les couleurs sont definies par :
# colour rgb(222, 100,33) par ex, utiliser : stroke="#969696"

s.anchor_x, s.anchor_y = 0, s.height
s2.anchor_x, s2.anchor_y = 0, s2.height
zoom = 1
angle = 30
draw_x = 300
draw_y = 200


def draw(canvas):
    background(0.1, 0.0, 0.1, 0.25)
    global angle
    angle += 1

    nofill()
    stroke(1, 1, 1, 0.2)
    strokewidth(0.5)
    s.draw(draw_x, draw_y, scale=3, angle=angle)
    s2.draw(draw_x, draw_y, scale=zoom, angle=angle)
     # Register mouse movement.
    if canvas.mouse.dragged:
        lines.append((LINETO, canvas.mouse.x, canvas.mouse.y, canvas.frame))
    elif canvas.mouse.pressed:
        lines.append((MOVETO, canvas.mouse.x, canvas.mouse.y, canvas.frame))

    if len(lines) > 0:
        for i in range(5):
            seed(i) # Lock the seed for smooth animation.
            p = BezierPath()
            for cmd, x, y, t in lines:
                d = sin((canvas.frame - t) / 10.0) * 10.0 # Play with the numbers.
                x += random(-d, d)
                y += random(-d, d)
                if cmd == MOVETO:
                    p.moveto(x, y)
                else:
                    p.lineto(x, y)
            drawpath(p)

canvas.fps = 60
canvas.size = 600, 400
#canvas.fullscreen = True
canvas.run(draw)

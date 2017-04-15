#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# simple pyglet animation - msarch@free.fr - december 2016

import math
import pyglet
from pyglet.gl import *

SCREEN = 1280, 800
ORIGIN = (640,400,0)
PI, TWOPI = math.pi, math.pi * 2
OMEGA = TWOPI * 0.5            # angular velocity (rev/s) : TWOPI/2 = 1/2 rev/s
alpha = 0.0                    # start angle

#--------------------------------- PYGLET STUFF -------------------------------
batch=pyglet.graphics.Batch()
canvas = pyglet.window.Window(width=SCREEN[0], height=SCREEN[1],fullscreen=True)
canvas.set_mouse_visible(False)
pyglet.clock.set_fps_limit(60)

glEnable(GL_LINE_SMOOTH)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # transparency ???
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glClearColor(0,0,0,0)            # background color

@canvas.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        pyglet.app.exit()
    elif symbol == pyglet.window.key.I:   # interraction
        toggle()

@canvas.event
def on_draw():
    canvas.clear()
    batch.draw()


#------------------------------- DRAWING STUFF --------------------------------
class Sketch(pyglet.graphics.Group):

    def __init__(self,pos=ORIGIN):
        super(Sketch, self).__init__()
        self.pos=pos

    def set_state(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)

    def unset_state(self):
        glPopMatrix()

    def clone(self):
        pass


#------------------------------- ACTION STUFF ---------------------------------
def update(dt, *args, **kwargs):
    # yelds sine and cosine values from an uniform circular motion
    global alpha
    alpha += dt * OMEGA
    alpha = alpha % (TWOPI)  # stay within [0,2*Pi]
    action1(dt, math.cos(alpha), math.sin(alpha))
    action2(dt, math.cos(alpha), math.sin(alpha))
    toggle(dt, math.cos(alpha), math.sin(alpha))


def action1(t,c,s):
        print "+ time, cos, sin = ", t,c,s

def action2(t,c,s):
        pass

def toggle(*args,**kwargs):
    #red_rec.vertices += 10
    # the color attribute of the vertex can be updated:
    blu_rec.colors[:3] = [int(200*args[1]), 0, 0, 255]
    red_rec.vertices[:2] = [int(200*args[1]),int(200*args[1])]

# red rectangle ---------------------------------------------------------------
g1= Sketch()
red_rec=batch.add(
        6,
        pyglet.gl.GL_TRIANGLES,
        g1,
        ('v2f/static',(0,0,0,100,100,100,100,100,100,0,0,0)),
        ('c4B/static', (255,0,0,230)*6)
        )
print "+ vertices = ", red_rec.vertices
print "+ vertices.count = ", red_rec.vertices.count

# blue triangle ---------------------------------------------------------------
# Since vertex lists are mutable, you may not necessarily want to initialise
# them with any particular data.
# You can specify just the format string in place of the (format, data) tuple
# in the data arguments vertex_list function.
# example : a vertex list of 3 vertices with positional and color attributes.

blu_rec=batch.add(
        3,
        pyglet.gl.GL_TRIANGLES,
        g1,
        'v2f/static',
        'c4B/static')

vtx2=[100,140,100,0,200,130]
clr2=(0,10,205,250)
blu_rec.vertices=[100,140,100,0,200,130]
blu_rec.colors = (0,0,255,230)*3


#----------------------------------- GO ---------------------------------------
if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()


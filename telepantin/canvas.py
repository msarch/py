#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# simple pyglet animation - msarch@free.fr - december 2016

import math
import pyglet
from pyglet.gl import *

SCREEN = 1280, 800
ORIGIN = (SCREEN[0]/2.0, SCREEN[1]/2.0,0)
PI, TWOPI = math.pi, math.pi * 2
BGCOLOR = (0,0,0,0)           # background color
SPEED = TWOPI / 2                # TWOPI/2 --> 1 engine revolution in 2 seconds

#--------------------------------- PYGLET STUFF -------------------------------
batch=pyglet.graphics.Batch()
canvas = pyglet.window.Window(width=SCREEN[0], height=SCREEN[1],fullscreen=True)
canvas.set_mouse_visible(False)

glEnable(GL_LINE_SMOOTH)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glClearColor(*BGCOLOR)
pyglet.clock.set_fps_limit(60)

@canvas.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        self.close()
    elif symbol == pyglet.window.key.I:
        pass  # invisibility toggle to be implemented as action                 TODO

@canvas.event
def on_draw():
    canvas.clear()
    batch.draw()


#------------------------------- DRAWING STUFF --------------------------------
class Sketch(pyglet.graphics.Group):

    def __init__(self, x=0, y=0, *args, **kwargs):
        super(Sketch, self).__init__(*args, **kwargs)
        self.x, self.y = x, y

    def set_state(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)

    def unset_state(self):
        glPopMatrix()

    def clone(self):
        pass

class Shape(pyglet.graphics.Vertex_list):

    def __init__(self, x=0, y=0, *args, **kwargs):
        super(Shape, self).__init__(*args, **kwargs)
        self.x, self.y = x, y

    def move(self, x=0, y=0):
        for i in xrange(0, len(self.vtx), 2):
            self.vtx[i] += x
            self.vtx[i + 1] += y
        self.vertex_list.vertices = self.vtx
        return(self)

        # don't forget to return self to be able to use short syntax
        #     sh=shape(...).translate(...)
        # rather than:
        #     sh=shape(....)
        #     sh.tranlate(...)


#------------------------------- ACTION STUFF ---------------------------------
pyglet.clock.schedule_interval(update, 1.0/60)

def update(dt):
    # yelds sine and cosine values from an uniform circular motion
    alpha += dt * omega
    alpha = alpha % (TWOPI)  # stay within [0,2*Pi]
    action1(dt , math.cos(alpha), math.sin(alpha))
    action2(dt , math.cos(alpha), math.sin(alpha))


def action1():
    pass

def action2():
    pass



# caroucell -------------------------------------------------------------------

##--- FILLED RECTANGLE --------------------------------------------------------
def rect(N=0, S=0, E=0, W=0):  # kapla default size
    """
    Rectangle, orthogonal, FILED, origin is bottom left
    N,S,E,W = north, south east, west coordinates
      _N_
    W|___|E
       S
    """
    vtx = [E, S, W, S, W, N, E, N]
    glstring = (4,
            pyglet.gl.GL_TRIANGLE_FAN,
            None,
            ('v2f/static', self.vtx),
            ('c4B/static', self.color * 4))
    return()


g1= Sketch(x=100,y=100)
string1 =(4,
        pyglet.gl.GL_TRIANGLE_FAN,
        g1,
        ('v2f/static',(0,0,0,40,100,40,100,0)),
        ('c4B/static', (155,155,0,155)*4)
        )
rec1=rect(10,10)

g2= Sketch(200,200)
string2=(4,
        pyglet.gl.GL_TRIANGLE_FAN,
        g2,
        ('v2f/static',(100,0,100,40,200,40,200,0)),
        ('c4B/static', (255,0,0,155)*4)
        )
rec2= Shape(string2,300,400)


if __name__ == "__main__":
    e=Engine()
    pyglet.app.run()


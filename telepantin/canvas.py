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
sketches=[]
batch=pyglet.graphics.Batch()

glEnable(GL_LINE_SMOOTH)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glClearColor(*BGCOLOR)

pyglet.clock.set_fps_limit(60)
#----------------------------------- CANVAS -----------------------------------
canvas = pyglet.window.Window(width=SCREEN[0], height=SCREEN[1],fullscreen=True)
canvas.set_mouse_visible(False)

@canvas.event
def on_key_press(self, symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        self.close()
    elif symbol == pyglet.window.key.I:
        pass  # invisibility toggle to be implemented as action                 TODO

@canvas.event
def on_key_press(symbol, modifiers):
    pyglet.app.exit()

@canvas.event
def on_draw():
    canvas.clear()
    batch.draw()

def update(dt):
    for engine in engines: engine.update(dt)
    draw()

#----------------------------------- SHAPE ------------------------------------
class Shape:
    def __init__(self,gl_string=None, x=0, y=0):
        #self.translate(x,y)
        pyglet.graphics.vertex_list=batch.add(*gl_string)

    def translate(self, x, y):
        for i in xrange(0, len(self.vtx), 2):
            self.vtx[i] += x
            self.vtx[i + 1] += y
        return (self)
        # don't forget to return self to be able to use short syntax
        #     sh=shape(...).tranlate(...)
        # rather than:
        #     sh=shape(....)
        #     sh.tranlate(...)


#----------------------------------- SKETCH -----------------------------------
class Sketch(pyglet.graphics.Group):

    def __init__(self, x=0, y=0, *args, **kwargs):
        super(Sketch, self).__init__(*args, **kwargs)
        self.x, self.y = x, y

    def set_state(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)

    def unset_state(self):
        glPopMatrix()


#----------------------------------- ENGINE -----------------------------------
class Engine():
    """
    each engine computes sine and cosine values of an uniform circular motion
    this movement then feeds the other actions

    """
    def __init__(self, *args, **kwargs):
        super(pyglet.graphics.Batch, self).__init__(*args, **kwargs)

    def setup(self, alpha=0, omega=SPEED, position=ORIGIN):
    # alpha = starting angle, omega = angular velocity in rev/sec
        self.shapes, self.actions = [], []
        self.alpha, self.omega, self.position = alpha, omega, position
        self.tt = 0.0  # total time
        self.cosalpha = math.cos(-self.alpha)
        self.sinalpha = math.sin(-self.alpha)

    def update(self, dt):
        engine.tt += dt
        engine.alpha += dt * engine.omega
        engine.alpha = engine.alpha % (TWOPI)  # stay within [0,2*Pi]
        engine.cosalpha = math.cos(engine.alpha)
        engine.sinalpha = math.sin(engine.alpha)
        for action in engine.actions:
            action.update(dt, tt=engine.tt)

    def plug(self, other):
        pass


# caroucell -------------------------------------------------------------------
##--- FILLED RECTANGLE --------------------------------------------------------
class Rect(Shape):
    """
    Rectangle, orthogonal, FILED, origin is bottom left
    N,S,E,W = north, south east, west coordinates
      _N_
    W|___|E
       S
    """

    def setup(self, N=0, S=0, E=0, W=0):  # kapla default size
        self.vtx = [E, S, W, S, W, N, E, N]
        self.glstring = (4,
                pyglet.gl.GL_TRIANGLE_FAN,
                None,
                ('v2f/static', self.vtx),
                ('c4B/static', self.color * 4))


g1= Sketch()
string1 =(4,
        pyglet.gl.GL_TRIANGLE_FAN,
        g1,
        ('v2f/static',(0,0,0,40,100,40,100,0)),
        ('c4B/static', (155,155,0,155)*4)
        )
rec= Shape(string1,10,10)

g2= Sketch(200,200)
string2=(4,
        pyglet.gl.GL_TRIANGLE_FAN,
        g2,
        ('v2f/static',(100,0,100,40,200,40,200,0)),
        ('c4B/static', (255,0,0,155)*4)
        )
rec2= Shape(string2,300,400)


if __name__ == "__main__":
    pyglet.app.run()


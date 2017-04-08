#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet
from pyglet.gl import *

# -----------------------------------------------------------------------------
window = pyglet.window.Window(width=800, height=600)
pyglet.gl.glClearColor(0, 0, 0, 0)
batch = pyglet.graphics.Batch()
ORIGIN= [400,300]

@window.event
def on_key_press(symbol, modifiers):
    pyglet.app.exit()

@window.event
def on_draw():
    window.clear()
    batch.draw()

# -----------------------------------------------------------------------------
class Sketch(pyglet.graphics.Group):

    def __init__(self, pos=ORIGIN, *args, **kwargs):
        super(Sketch, self).__init__(*args, **kwargs)
        self.pos = pos

    def set_state(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)

    def unset_state(self):
        glPopMatrix()


# -----------------------------------------------------------------------------
g1= Sketch()
string1 =(3,
        pyglet.gl.GL_TRIANGLES,
        g1,
        ('v2f/static',(0,0,0,100,100,400)),
        ('c4B/static', (255,0,0,0)*3)
        )
string2 =(3,
        pyglet.gl.GL_TRIANGLES,
        g1,
        ('v2f/static',(-100,-140,-100,0,-200,-130)),
        ('c4B/static', (0,10,205,0)*3)
        )
red_rec=batch.add(*string1)
red_rec=batch.add(*string2)

# from : https://groups.google.com/forum/#!topic/pyglet-users/vQFlo0HtpUA
# You can easily draw several discontinuous shapes in a single GL_TRIANGLES
# primitive. This is not possible using GL_TRIANGLE_STRIPs or FANs.

# Because of the way the graphics API renders multiple primitives with
# shared state, GL_POLYGON, GL_LINE_LOOP and GL_TRIANGLE_FAN cannot be
# used --- the results are undefined.

# When using GL_LINE_STRIP, GL_TRIANGLE_STRIP or GL_QUAD_STRIP care must
# be taken to insert degenrate vertices at the beginning and end of each
# vertex list. For example, given the vertex list:
# A, B, C, D
# the correct vertex list to provide the vertex list is:
# A, A, B, C, D, D

g2= Sketch()
string3=(6,
        pyglet.gl.GL_TRIANGLE_FAN,
        g1,
        ('v2f/static',(0,100,0,100,0,140,100,140,100,100,100,100)),
        ('c4B/static', (0,0,255,0)*6)
        )
rec2=batch.add(*string3)

points=batch.add(2, pyglet.gl.GL_POINTS, g1,
        ('v2i', (200, -115, 300, 135)),
        ('c3B', (255, 0, 255, 0, 255, 0))
        )

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    pyglet.app.run()


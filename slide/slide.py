#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# ms; 06.2016; simple pyglet anim

##  IMPORTS -------------------------------------------------------------------
import pyglet
import random
import math
import pyglet.gl as GL

##  CONSTANTS AND VARIABLES ---------------------------------------------------
kapla_colors = [(1.00, 0.84, 0.00),(0.00, 0.39, 0.00), (0.00, 0.39, 0.00),
        (1.00, 0.27, 0.00), (0.00, 0.00, 0.55)]
WHITE = ( 1.00,1,1)
ORIGIN = (0, 0)  # default x,y
XMAX, YMAX, FPS = 1280, 800, 60  # screen x,y dimensions, target FPS for anim.
TWOPI = math.pi*2

##  CANVAS --------------------------------------------------------------------
class Canvas(pyglet.window.Window):
    """ pyglet windows, runs a constant circular motion
    yelds sine and cosine (scotch and yoke)
    usable as anchors for harmonic oscillationsalong X and Y axis
    """
    def __init__(self, xmax, ymax, fps):
        pyglet.window.Window.__init__(self,fullscreen=True)
        self.set_mouse_visible(False)
        self.xmax, self.ymax, self.fps = xmax, ymax, fps
        self.shapes, self.actions = [], []
        self.omega = 0.5*TWOPI  #angular velocity
        self.alpha = 0.0  #start angle

        pyglet.clock.schedule_interval(self.update, 1.0/fps)
        GL.glTranslatef(self.xmax/2,self.ymax/2, 0.0)  # Origin > screen center
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)  # set background color to black

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            exit()

    def draw(self):
        self.clear()                    # clear graphics
        for shape in self.shapes:
            GL.glPushMatrix()
            GL.glTranslatef(shape.pos[0], shape.pos[1], 0)
            shape.batch.draw()  # * expands list (no append method)
            GL.glPopMatrix()

    def update(self,dt):
        self.alpha += dt * self.omega
        self.alpha = self.alpha % (TWOPI)  # stay within [0,2*Pi]
        self.scotch, self.yoke = math.sin(self.alpha), math.cos(self.alpha)
        for action in self.actions:
            action.update(dt)
        self.draw()


##--- SIMPLE RECTANGLE (ortho) ------------------------------------------------
class Rect(object):
    """ recs attributes : size, color, path, position on path  """
    def __init__(self, S=0, E=0, N=100, W=300, color=WHITE):
        self.vtx=[E, S, W, S, W, N, E, N]
        self.color = color
        self.pos = ORIGIN
        self.getbatch()

    def getbatch(self):
        self.batch = pyglet.graphics.Batch()
        self.batch.add(4,pyglet.gl.GL_TRIANGLE_FAN, None, ('v2i/static',
        self.vtx))
        # batch rendering list : number of vertexes, GL primtype, ???,
        # type and list of vertexes, type and list of colors

class Blip(object):
    """Point, autocad style"""
    def __init__(self):
        self.pos = ORIGIN
        self.vtx=[-3,0,3,0,0,0,0,3,0,-3]
        self.getbatch()

    def getbatch(self):
        self.batch = pyglet.graphics.Batch()
        self.batch.add(5,pyglet.gl.GL_LINE_STRIP, None, ('v2i/static',
        self.vtx))

class Scotchyoke(object):
    """ links the object position to canvas circular motion"""
    def __init__(self,target=None, Xrange=1, Yrange=1):
        self.target, self.Xrange, self.Yrange  = target, Xrange, Yrange

    def update(self,dt):
        self.target.pos = (canvas.scotch*self.Xrange,canvas.yoke*self.Yrange)
        print 1/dt


# SCENE SETUP -----------------------------------------------------------------
def move(target, x, y):
    for  i in xrange(0,len(target.vtx),2):
        target.vtx[i] += x
        target.vtx[i+1] += y
        target.getbatch()

def setup(canvas):
    g = int(canvas.ymax/85)
    e = 6*g
    w = 11*g
    h = 33*g

    r = Rect(color=random.choice(kapla_colors))
    move(r,-150,0)
    b = Blip()
    canvas.shapes.extend((r,b))

#  use vtx as standard for rect and blip
    s =Scotchyoke(target=b, Xrange=XMAX/2,Yrange=XMAX/2)
    t =Scotchyoke(target=r, Xrange=XMAX/2-150,Yrange=0)
    canvas.actions.extend((s,t))

##  MAIN ----------------------------------------------------------------------
if __name__ == "__main__":
    canvas = Canvas(XMAX,YMAX,FPS)  # screen size xmax, ymax, FPS
    setup(canvas)
    pyglet.app.run()


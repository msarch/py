#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#''''' ''
"""simple pyglet animation, ms, 07-2016 """

import pyglet
import math
import pyglet.gl as GL

XMAX, YMAX, FPS = 1280.0, 800.0, 60  # screen x,y dimensions, target FPS for anim.
PI, TWOPI = math.pi, math.pi*2
K1, K2, K3 = 6, 11, 33  # kapla size (mm)
XRAD = ((K3+K1+K2+K3+K1)/2-K3/2)+K3/2-K2/2
YRAD = (K3+K1+K2+K3+K1)/2-K3/2

##  CANVAS -------------------------------------------------------------------
class Canvas(pyglet.window.Window):
    """
    pyglet window
    running following sets, in that order: engines, actions, observers
    displaying : list of shapes
    """
    def __init__(self, xmax, ymax, fps):
        pyglet.window.Window.__init__(self,fullscreen=True)
        self.set_mouse_visible(False)
        self.xmax, self.ymax, self.fps = xmax, ymax, fps
        self.engines, self.shapes, self.actions, self.observers = [], [], [], []

        self.x, self.y = 0, 0
        self.target_x, self.target_y = self.x, self.y
        self.scale = 85
        self.target_scale = self.scale

        pyglet.clock.schedule_interval(self.update, 1.0/fps)
        GL.glTranslatef(self.xmax/2,self.ymax/2, 0.0)  # Origin > screen center
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)  # set background color to black

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:self.close()
        elif symbol == pyglet.window.key.PAGEUP: self.camera_zoom(1.25)
        elif symbol == pyglet.window.key.PAGEDOWN: self.camera_zoom(0.8)
        elif symbol == pyglet.window.key.LEFT: self.camera_pan(self.scale/2, 0)
        elif symbol == pyglet.window.key.RIGHT: self.camera_pan(-self.scale/2, 0)
        elif symbol == pyglet.window.key.DOWN: self.camera_pan(0, self.scale/2)
        elif symbol == pyglet.window.key.UP: self.camera_pan(0, -self.scale/2)

    def camera_update(self):  # update reaches target in ten times
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1
        self.scale += (self.target_scale - self.scale) * 0.1

    def camera_zoom(self, factor):
        self.target_scale *= factor

    def camera_pan(self, dx,dy):
        self.target_x += dx
        self.target_y += dy

    def camera_focus(self, width, height):
        "Set projection and modelview matrices ready for rendering"
        # Set projection matrix suitable for 2D rendering"
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        a = width / height
        GL.gluOrtho2D(-self.scale * a, self.scale * a, -self.scale, self.scale)

       # Set modelview matrix to move & scale to camera position"
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.gluLookAt(self.x, self.y, 1.0, self.x, self.y, -1.0, 0.0, 1.0, 0.0)

    def draw(self):
        # Camera stuff mostly from Jonathan Hartley (tartley@tartley.com)
        # demos 'stretching pyglets wings'
        self.clear()
        self.camera_update()
        self.camera_focus(self.xmax, self.ymax)

        for s in self.shapes:
            GL.glPushMatrix()
            GL.glTranslatef(s.pos[0], s.pos[1], 0)
            s.batch.draw()  # * expands list (no append method)
            GL.glPopMatrix()

    def update(self,dt):
        for e in self.engines:
            e.update(dt)
        for a in self.actions:
            a.update(dt)
        for o in self.observers:
            o.update(dt)
        self.draw()


##--- ROTATING ENGINE ---------------------------------------------------------
class Engine(object):
    """
    will keep updating sine and cosine values of a uniform circular motion
    starting at angle : alpha
    angular velocity (per sec) : omega
    """
    def __init__(self, alpha=0.0, omega=0.5*TWOPI):
        self.alpha,self.omega = alpha,omega # start angle, angular velocity
        self.cosa, self.sina = math.cos(self.alpha), math.sin(self.alpha)

    def update(self,dt):
        self.alpha += dt * self.omega
        self.alpha = self.alpha % (TWOPI)  # stay within [0,2*Pi]
        # updates 2 coordinates with an harmonic linear osillation
        self.cosa, self.sina = math.cos(self.alpha), math.sin(self.alpha)


##--- SHAPES SECTION ----------------------------------------------------------
class Shape(object):
    def setup(self):
        if not hasattr(self,'pos'): self.pos=(0,0)
        if not hasattr(self,'vtx'): self.vtx=[0,0]
        # in this list vtx coordinates are flatened: [x0,y0,x1,y1,x2,y2...etc.]
        if not hasattr(self,'color'): self.color=(0,0,0)
        if not hasattr(self,'glstring'): self.glstring=(
                2,pyglet.gl.GL_LINES, None, ('v2f/static',0,0,1,1))
        self.getbatch()

    def getbatch(self):
        self.batch = pyglet.graphics.Batch()
        self.batch.add(*self.glstring)

    def translate(self, x, y):
        for i in xrange(0,len(self.vtx),2):
            self.vtx[i] += x
            self.vtx[i+1] += y
            self.getbatch()
        return(self)
        # don't forget to return self to be able to use short syntax
        #     sh=shape(...).tranlate(...)
        # rather than:
        #     sh=shape(....)
        #     sh.tranlate(...)

    # usually not used but will update batch if necessary
    # ie: in case positions of the end points of a Line are modified.
    def update(self,dt):
        self.getbatch()


class Point(Shape):
    """
    Simple Point, Autocad style cross
    """
    def __init__(self):
        self.vtx=[-3,0,3,0,0,0,0,3,0,-3]
        self.glstring=(5,pyglet.gl.GL_LINE_STRIP, None, ('v2i/static',self.vtx))
        self.setup()


class Line(Shape):
    """
    Simple line defined by 2 points
    """
    def __init__(self,p1=Point(),p2=Point()):
        self.p1, self.p2 = p1, p2
        self.glstring=(2,pyglet.gl.GL_LINES, None, ('v2f/static',
            (self.p1.pos[0],self.p1.pos[1],self.p2.pos[0],self.p2.pos[1])))
        self.setup()


class Rect(Shape):
    """
    Rectangle, orthogonal, origin is bottom left
    """
    def __init__(self, S=0, E=0, N=K2, W=K3):  #kapla default size
        self.vtx=[E, S, W, S, W, N, E, N]
        self.glstring=(4,pyglet.gl.GL_TRIANGLE_FAN, None, ('v2f/static',
        self.vtx))
        self.setup()


class Circle(Shape):
    """
    Circle, outline only
    """
    def __init__(self,radius=100):
        # nov = number of divisions per ∏ rads (half the circle)
        # with vertices numbered like a clock,  GL_TRIANGLE_STRIP order is:
        # 11, 12, 10, 1, 9, 2, 8, 3, 7, 4, 6, 5
        self.radius=radius
        self.vtx=[0, self.radius]  #create list and first element
        stepangle = PI/(int(self.radius/5)+12)
        phi=0
        while phi<TWOPI:
            self.vtx.append(self.radius * math.sin(phi))
            self.vtx.append(self.radius * math.cos(phi))
            phi += stepangle
        self.vtx.extend([0,self.radius])  # add right side vertex
        n=int(len(self.vtx)/2)
        self.glstring=(n,pyglet.gl.GL_LINE_STRIP, None, ('v2f/static',
        self.vtx))
        self.setup()


##--- CROSSHAIR VERTICAL
class Vline(Shape):
    def __init__(self):
        self.vtx=[0,0] # x only
        self.glstring=(2,pyglet.gl.GL_LINES, None, ('v2f/static',
        (self.vtx[0],-YMAX,self.vtx[0],YMAX)))
        self.setup()


##--- CROSSHAIR HORIZONTAL
class Hline(Shape):
    def __init__(self):
        self.vtx=[0,0]
        self.glstring=(2,pyglet.gl.GL_LINES, None, ('v2f/static',
        (-XMAX, self.vtx[1],XMAX,self.vtx[1])))
        self.setup()


##--- ACTIONS -----------------------------------------------------------------
#--- HARMONIC OSILLATION
class Scotchyoke(object):
    """ links target X or Y coordinate to canvas circular motion generator"""
    def __init__(self,engine,target=None,Hradius=1,Vradius=1,center=(0,0),phase=0):
        self.e=engine
        self.target = target
        self.Hradius, self.Vradius  = Hradius, Vradius
        self.dx,self.dy=center
        self.cosb, self.sinb = math.cos(phase), math.sin(phase)

    def update(self,dt):
        #cos(A+B)=cos A cos B - sin A sin B
        cosab=self.e.cosa*self.cosb-self.e.sina*self.sinb
        #sin(A+B)=sin A cos B + cos A sin B
        sinab=self.e.sina*self.cosb+self.e.cosa*self.sinb
        self.target.pos=(self.dx+cosab*self.Hradius,self.dy+sinab*self.Vradius)


##--- OBSERVERS SECTION -------------------------------------------------------
#--- CHANGE COLOR ON BOUNCE
class reverse_dir(object):
    def __init__(self,target=None):
        self.target = target
        self.previous=self.target.pos
        self.dirx=0

    def update(self,dt):
        newdir = cmp(self.target.pos[0],self.previous[0])
        if newdir == self.dirx:
            pass
        else:
            self.dirx = newdir
            print self.target, "reversed dir x"


## SCENE SETUP ----------------------------------------------------------------
def setup(canvas):
    # engines -----------------------------------------------------------------
    e=Engine()
    canvas.engines.append(e)

    # moving objects ----------------------------------------------------------
    #    . o
    #  . . -
    #  o |
    r1 = Rect().translate(-K3/2,-K2/2)   #sliding, horizontal
    l1 = Vline()                         #moving with r1
    l1a = Vline()                        #moving with r1
    c1 = Circle(radius=K3/2)             #moving with r1
    canvas.shapes.extend((r1,l1,l1a,c1))

    r2 = Rect(N=K3,W=K2).translate(-K2/2,-K3/2)   #sliding, vertical
    l2 = Hline()                                  #moving with r2
    l2a = Hline()                                 #moving with r2
    c2 = Circle(radius=K3/2)                      #moving with r2
    canvas.shapes.extend((r2,l2,l2a,c2))

    s1 = Scotchyoke(e, target=r1, Hradius=XRAD, Vradius=0, center=(0,0))
    s2 = Scotchyoke(e, target=l1, Hradius=XRAD, Vradius=0, center=(K3/2,0))
    s2a= Scotchyoke(e, target=l1a, Hradius=XRAD, Vradius=0, center=(-K3/2,0))
    s3 = Scotchyoke(e, target=c1, Hradius=XRAD, Vradius=XRAD)
    canvas.actions.extend((s1,s2,s2a,s3))

    s4 = Scotchyoke(e, target=r2, Hradius=0, Vradius=YRAD, phase=PI)
    s5 = Scotchyoke(e, target=l2, Hradius=0, Vradius=YRAD, center=(0,K3/2), phase=PI)
    s5a= Scotchyoke(e, target=l2a, Hradius=0, Vradius=YRAD, center=(0,-K3/2), phase=PI)
    s6 = Scotchyoke(e, target=c2, Hradius=YRAD, Vradius=YRAD, phase=PI)
    canvas.actions.extend((s4,s5,s5a,s6))

    # observers ---------------------------------------------------------------
    o1=reverse_dir(target=r1)  #check if shape has gone reverse
    canvas.observers.append((o1))

    # still objects -----------------------------------------------------------
    #  _||_
    #  -  -
    #   ||
    r11 = Rect(N=K3,W=K1).translate(-K1-K2/2,K2/2+K1)          #vertical top left
    r12 = Rect(N=K3,W=K1).translate(K2/2,K2/2+K1)             #vertical top right
    r13 = Rect(N=K3,W=K1).translate(-K2/2-K1,-K3-K2/2-K1-1)     #vertical bottom left
    r14 = Rect(N=K3,W=K1).translate(K2/2,-K3-K2/2-K1-1)        #vertical bottom right

    r21 = Rect(N=K1,W=K3).translate(K2/2+K1,K2/2)         #horizontal top right
    r22 = Rect(N=K1,W=K3).translate(K2/2+K1,-K1-K2/2-1)    #horizontal bottom right
    r23 = Rect(N=K1,W=K3).translate(-K3-K2/2-K1,K2/2)      #horizontal top left
    r24 = Rect(N=K1,W=K3).translate(-K3-K2/2-K1,-K1-K2/2-1) #horizontal bottom left

    pt = Point()
    canvas.shapes.extend((r11,r12,r13,r14,r21,r22,r23,r24,pt))

##  MAIN ----------------------------------------------------------------------
if __name__ == "__main__":
    canvas = Canvas(XMAX,YMAX,FPS)  # screen size, FPS
    setup(canvas)
    pyglet.app.run()

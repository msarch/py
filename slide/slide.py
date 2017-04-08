#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#''''' ''
"""simple pyglet animation, ms, 07-2016 """

import pyglet
import math
import pyglet.gl as GL

SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 1280, 800, 60
PI, TWOPI = math.pi, math.pi*2
SPEED=TWOPI/2  # TWOPI/2 --> 1 engine revolution in 2 seconds

BOW = pyglet.media.load('bow.wav', streaming=False)
BOW1 = pyglet.media.load('bow1.wav', streaming=False)
BOW.play()

##  CANVAS -------------------------------------------------------------------
class Canvas(pyglet.window.Window):
    """
    pyglet window
    running following sets, in that order: engines, actions, observers
    displaying : list of shapes
    """
    def __init__(self, w=SCREEN_WIDTH, h=SCREEN_HEIGHT, fps=FPS,
            alpha=0, omega=SPEED):
        pyglet.window.Window.__init__(self,fullscreen=True)
        self.set_mouse_visible(False)
        self.soundon=1
        self.w, self.h, self.fps = 1.0*w, 1.0*h, fps
        self.layers, self.actions, self.observers = [], [], []
        self.i_layers = [] # those layers visibility is toggled by key 'I'
        self.alpha, self.omega = alpha, omega # start angle, angular velocity
        self.cosalpha, self.sinalpha = math.cos(-self.alpha), math.sin(-self.alpha)

        # camera stuff
        self.x, self.y = 0, 0
        self.scale = 100
        self.ratio= self.w/self.h
        self.target_x, self.target_y = self.x, self.y
        self.target_scale = self.scale

        self.setup_gl()
        pyglet.clock.schedule_interval(self.update, 1.0/fps)

    def setup_gl(self):
        """Set various pieces of OpenGL state for better rendering of SVG.

        """
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glTranslatef(0.5*self.w, 0.5*self.h, 0.0)  # Origin > screen center
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)  # set background color to black

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:self.close()
        elif symbol == pyglet.window.key.PAGEDOWN: self.camera_zoom(1.25)
        elif symbol == pyglet.window.key.PAGEUP: self.camera_zoom(0.8)
        elif symbol == pyglet.window.key.LEFT: self.camera_pan(self.scale/2,0)
        elif symbol == pyglet.window.key.RIGHT: self.camera_pan(-self.scale/2,0)
        elif symbol == pyglet.window.key.DOWN: self.camera_pan(0, self.scale/2)
        elif symbol == pyglet.window.key.UP: self.camera_pan(0, -self.scale/2)
        elif symbol == pyglet.window.key.S: self.soundon = not self.soundon
        elif symbol == pyglet.window.key.I:
            for l in self.i_layers: l.visible =not l.visible

    # camera ------------------------------------------------------------------
        # Camera stuff mostly from Jonathan Hartley (tartley@tartley.com)
        # demo's stretching pyglets wings
    def camera_zoom(self, factor):
        self.target_scale *= factor

    def camera_pan(self, dx,dy):
        self.target_x += dx
        self.target_y += dy

    def camera_update(self):  # update reaches target in ten times
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1
        self.scale += (self.target_scale - self.scale) * 0.1

    def camera_focus(self):
        "Set projection and modelview matrices ready for rendering"
        # Set projection matrix suitable for 2D rendering"
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        	# GL.gluOrtho2D(left,right,bottom,top)
        GL.gluOrtho2D(
                -self.scale * self.ratio,
                self.scale * self.ratio,
                -self.scale,
                self.scale)
        # Set modelview matrix to move & scale to camera position"
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.gluLookAt(self.x, self.y, 1.0, self.x, self.y, -1.0, 0.0, 1.0, 0.0)


    # engine ------------------------------------------------------------------
    def engine_update(self,dt):
        """
        updates sine and cosine values in a uniform circular motion
        starting at angle : alpha
        angular velocity (per sec) : omega
        """
        self.alpha += dt * self.omega
        self.alpha = self.alpha % (TWOPI)  # stay within [0,2*Pi]
        # updates 2 coordinates with an harmonic linear osillation
        self.cosalpha, self.sinalpha = math.cos(self.alpha), math.sin(self.alpha)

    def draw(self):
        self.clear()
        self.camera_update()
        self.camera_focus()
        for l in self.layers: l.draw()

    def update(self,dt):
        self.engine_update(dt)
        for action in self.actions: action.update(dt)
        for observer in self.observers: observer.update(dt)
        self.draw()

##--- DEFINE UNIQUE CANVAS HERE -----------------------------------------------
canvas = Canvas()

##--- LAYERS SECTION ----------------------------------------------------------
class Layer(object):
    """
    group of displayed elements
    """
    def __init__(self,posx=0,posy=0, visible=True):
        self.posx, self.posy= posx, posy
        self.shapes = []
        self.visible=visible
        canvas.layers.append(self)

    def toggles(self):
        canvas.i_layers.append(self)

    def draw(self):
        if self.visible:
                GL.glPushMatrix()
                GL.glTranslatef(self.posx, self.posy, 0)
                for s in self.shapes:
                    s.draw()  # * expands list (no append method)
                GL.glPopMatrix()

    def move(self,dx,dy):
        self.posx += dx
        self.posy += dy


##--- DEFINE DEFAULT LAYER HERE -----------------------------------------------
layer_0=Layer()

##--- SHAPES SECTION ----------------------------------------------------------
class Shape(object):
    """
    superclass for displayed elements
    """
    def setup(self):
        if not hasattr(self,'layer'): self.layer=layer_0
        if not hasattr(self,'pos'): self.pos=(0,0)
        if not hasattr(self,'vtx'): self.vtx=[0,0]
        # in this list vtx coordinates are flatened: [x0,y0,x1,y1,x2,y2...etc.]
        if not hasattr(self,'color'): self.color=(0,0,0)
        if not hasattr(self,'glstring'): self.glstring=(
                2,pyglet.gl.GL_LINES, None, ('v2f/static',0,0,1,1))
        if not hasattr(self,'batch'): self.getbatch()

    def getbatch(self):
        self.batch = pyglet.graphics.Batch()
        self.batch.add(*self.glstring)

    def draw(self):
        GL.glPushMatrix()
        GL.glTranslatef(self.pos[0], self.pos[1], 0)
        self.batch.draw()  # * expands list (no append method)
        GL.glPopMatrix()

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
        self.glstring=(5,pyglet.gl.GL_LINE_STRIP, None, ('v2i/static',
            self.vtx))
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
    Rectangle, orthogonal, FILED, origin is bottom left
    N,S,E,W = north, south east, west coordinates
      _N_
    W|___|E
       S
    """
    def __init__(self, N=0, S=0, E=0, W=0):  #kapla default size
        self.vtx=[E, S, W, S, W, N, E, N]
        self.glstring=(4,pyglet.gl.GL_TRIANGLE_FAN, None, ('v2f/static',
        self.vtx))
        self.setup()


class Rect2(Shape):
    """
    Rectangle, orthogonal, OUTLINE ONLY, origin is bottom left
    """
    def __init__(self, S=0, E=0, N=0, W=0):  #kapla default size
        self.vtx=[E, S, W, S, W, N, E, N, E, S]
        self.glstring=(5,pyglet.gl.GL_LINE_STRIP, None, ('v2f/static',
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
    """
    fullscreen vertical line
    """
    def __init__(self):
        self.vtx=[0,0] # x only
        self.glstring=(2,pyglet.gl.GL_LINES, None, ('v2f/static',
        (self.vtx[0],-SCREEN_HEIGHT,self.vtx[0],SCREEN_HEIGHT)))
        self.setup()


##--- CROSSHAIR HORIZONTAL
class Hline(Shape):
    """
    fullscreen horizontal line
    """
    def __init__(self):
        self.vtx=[0,0]
        self.glstring=(2,pyglet.gl.GL_LINES, None, ('v2f/static',
        (-SCREEN_WIDTH, self.vtx[1],SCREEN_WIDTH,self.vtx[1])))
        self.setup()


##--- ACTIONS -----------------------------------------------------------------
#--- HARMONIC OSILLATION
class Scotchyoke(object):
    """
    modifies target X or Y coordinate to match canvas circular motion generator
    """
    def __init__(self,target,Hradius=0,Vradius=0,center=(0,0),direction=1,phase=0):
        self.target = target
        self.Hradius, self.Vradius  = Hradius, Vradius
        self.dx,self.dy=center
        self.cosb, self.sinb = math.cos(phase)*direction, math.sin(phase)
        cosa, sina = canvas.cosalpha, canvas.sinalpha

    def update(self,dt):
        #cos(A+B)=cos A cos B - sin A sin B
        cosab=canvas.cosalpha*self.cosb-canvas.sinalpha*self.sinb
        #sin(A+B)=sin A cos B + cos A sin B
        sinab=canvas.sinalpha*self.cosb+canvas.cosalpha*self.sinb
        #set target position
        self.target.pos=(self.dx+cosab*self.Hradius,self.dy+sinab*self.Vradius)


##--- OBSERVERS SECTION -------------------------------------------------------
#--- CHANGE COLOR ON BOUNCE
class reverse_dir(object):
    """
    Checks for each axis if direction of target motion has changed
    """
    def __init__(self,target=None):
        self.target = target
        self.previous=self.target.pos
        self.dirx, self.diry = 0, 0

    def update(self,dt):
        newdirx = cmp(self.target.pos[0],self.previous[0])
        newdiry = cmp(self.target.pos[1],self.previous[1])
        if newdirx != self.dirx:
            self.dirx = newdirx
            if canvas.soundon : BOW.play()

            print self.target, "reversed dir x"
        elif newdiry != self.diry:
            self.diry = newdiry
            if canvas.soundon : BOW1.play()

            print self.target, "reversed dir y"
        else:
            pass

## SCENE SETUP ----------------------------------------------------------------
class Heart(object):
    """
    cell,
    K1,K2,K3 are real life kapla dimensions in mm
    movement fits the extents dimensions N,S,E,W (north, south east, west)
    """
    def __init__(self,layer=layer_0,
            K1=6,K2=11,K3=34,
            north=94, south=0,east=94,west=0,
            hdir=1,hphase=0,vdir=1,vphase=0):

        Y_RAD = (north-south)/2-K3/2  #extends of the giration
        X_RAD = (east-west)/2-K3/2

        # moving objects ------------------------------------------------------
        #    . o
        #  . . -
        #  o |
        # sliding rect, horizontal
        r1 = Rect(N=K1,W=K3).translate(-K3/2,-K1/2)  #r1 horizontal sliding
        r2 = Rect(N=K3,W=K1).translate(-K1/2,-K3/2)  #r2 vertical sliding
        layer.shapes.extend((r1,r2))
        # movement
        s1 = Scotchyoke(r1, Hradius=X_RAD, Vradius=0, center=(0,0),direction=hdir,phase=hphase)
        s2 = Scotchyoke(r2, Hradius=0, Vradius=Y_RAD, direction=vdir, phase=vphase)
        canvas.actions.extend((s1,s2))

        # observers ---------------------------------------------------------------
        o1=reverse_dir(target=r1)  #check if r1 has gone reverse
        o2=reverse_dir(target=r2)  #check if r2 has gone reverse
        canvas.observers.extend((o1,o2))

        # still objects -----------------------------------------------------------
        #  _||_
        #  -  -
        #   ||
        #verticals
        r11 = Rect(N=K3,W=K2).translate(-K2-K1/2,K1/2+K2)         #top left
        r12 = Rect(N=K3,W=K2).translate(K1/2,K1/2+K2)             #top right
        r13 = Rect(N=K3,W=K2).translate(-K1/2-K2,-K3-K1/2-K2)   #bottom left
        r14 = Rect(N=K3,W=K2).translate(K1/2,-K3-K1/2-K2)       #bottom right
        layer.shapes.extend((r11,r12,r13,r14))
        # horizontals
        r21 = Rect(N=K2,W=K3).translate(K1/2+K2,K1/2)             #top right
        r22 = Rect(N=K2,W=K3).translate(K1/2+K2,-K2-K1/2)       #bottom right
        r23 = Rect(N=K2,W=K3).translate(-K3-K1/2-K2,K1/2)         #top left
        r24 = Rect(N=K2,W=K3).translate(-K3-K1/2-K2,-K2-K1/2)   #bottom left
        layer.shapes.extend((r21,r22,r23,r24))


class Heart_Mechanics(object):
    """
    hidden mechanism behind the scene with same args, goes on a toggle layer
    """
    def __init__(self,layer=layer_0,
            K1=6,K2=12,K3=33,
            north=94, south=0,east=94,west=0,
            hdir=1,hphase=0,vdir=1,vphase=0):

        Y_RAD = (north-south)/2-K3/2  #extends of the giration
        X_RAD = (east-west)/2-K3/2
        # shapes
        rc1 = Rect2(N=north/2, S=-north/2, W=K3)  #slot for r1
        rc2 = Rect2(W=east/2, E=-east/2, N=K3/2, S=-K3/2)  #r2 slot
        c1 = Circle(radius=K3/2)  #peg for slot 1 movement
        c2 = Circle(radius=K3/2)  #peg for slot 2 movement
        layer.shapes.extend((c1,c2,rc1,rc2))
        # movement
        s3 = Scotchyoke(c1, Hradius=X_RAD, Vradius=Y_RAD, direction=hdir, phase=hphase)
        s4 = Scotchyoke(c2, Hradius=Y_RAD, Vradius=Y_RAD, direction=vdir, phase=vphase)
        s5 = Scotchyoke(rc1, Hradius=X_RAD, Vradius=0, center=(-K3/2,0), direction=hdir, phase=hphase)
        s6 = Scotchyoke(rc2, Hradius=0, Vradius=Y_RAD, direction=vdir, phase=vphase)
        canvas.actions.extend((s3,s4,s5,s6))
        #outside frame
        rc = Rect2(W=east/2, E=-east/2, N=north/2, S=-north/2)
        layer.shapes.append((rc))


##  MAIN ----------------------------------------------------------------------
if __name__ == "__main__":

    # layers ------------------------------------------------------------------
    layer_1=Layer(visible=True)
    layer_1.move(0,0)  #move aside half a cell

    layer_1a=Layer(visible=True)
    layer_1a.move(-96,-96)

    layer_1b=Layer(visible=True)
    layer_1b.move(-96,96)

    layer_1c=Layer(visible=True)
    layer_1c.move(96,96)

    layer_1d=Layer(visible=True)
    layer_1d.move(96,-96)

    layer_m1=Layer(visible=False)
    layer_m1.move(0,0)
    layer_m1.toggles()

    layer_m1a=Layer(visible=False)
    layer_m1a.move(-96,-96)
    layer_m1a.toggles()

    layer_m1b=Layer(visible=False)
    layer_m1b.move(-96,96)
    layer_m1b.toggles()

    layer_m1c=Layer(visible=False)
    layer_m1c.move(96,96)
    layer_m1c.toggles()

    layer_m1d=Layer(visible=False)
    layer_m1d.move(96,-96)
    layer_m1d.toggles()

    #C2 type-----------------------------
    layer_2=Layer(visible=True)
    layer_2.move(96,0)

    layer_2a=Layer(visible=True)
    layer_2a.move(-96,0)

    layer_2b=Layer(visible=True)
    layer_2b.move(0,96)

    layer_2c=Layer(visible=True)
    layer_2c.move(0,-96)

    layer_m2=Layer(visible=False)
    layer_m2.move(96,0)
    layer_m2.toggles()

    layer_m2a=Layer(visible=False)
    layer_m2a.move(-96,0)
    layer_m2a.toggles()

    layer_m2b=Layer(visible=False)
    layer_m2b.move(0,96)
    layer_m2b.toggles()

    layer_m2c=Layer(visible=False)
    layer_m2c.move(0,-96)
    layer_m2c.toggles()

    # cells -------------------------------------------------------------------
    # c1 has thin sliders: K1,K2,K3=6,11,34. total figure size = 96x96
    # (K3+K2+K1+K2+K3 = size of the cell)
    # c2 has thick sliders (11), K1,K2,K3=11,6,34 total figure size = 91x91
    c1=Heart(layer=layer_1,K1=6,K2=11,K3=34,north=96,east=96,
            hdir=1,hphase=0,vdir=1,vphase=0)
    mc1=Heart_Mechanics(layer=layer_m1,K1=6,K2=11,K3=34,north=96,east=96,
            hdir=1,hphase=0,vdir=1,vphase=0)

    c1a=Heart(layer=layer_1a,K1=6,K2=11,K3=34,north=96,east=96,
            hdir=1,hphase=0,vdir=1,vphase=0)
    mc1a=Heart_Mechanics(layer=layer_m1a,K1=6,K2=11,K3=34,north=96,east=96,
            hdir=1,hphase=0,vdir=1,vphase=0)

    c1b=Heart(layer=layer_1b,K1=6,K2=11,K3=34,north=96,east=96,
            hdir=1,hphase=0,vdir=1,vphase=PI/4)
    mc1b=Heart_Mechanics(layer=layer_m1b,K1=6,K2=11,K3=34,north=96,east=96,
            hdir=1,hphase=0,vdir=1,vphase=PI/4)

    c1c=Heart(layer=layer_1c,K1=6,K2=11,K3=34,north=96,east=96,
            hdir=1,hphase=PI/8,vdir=1,vphase=0)
    mc1c=Heart_Mechanics(layer=layer_m1c,K1=6,K2=11,K3=34,north=96,east=96,
            hdir=1,hphase=PI/8,vdir=1,vphase=0)

    c1d=Heart(layer=layer_1d,K1=6,K2=11,K3=34,north=96,east=96,
            hdir=1,hphase=0,vdir=1,vphase=PI/12)
    mc1d=Heart_Mechanics(layer=layer_m1d,K1=6,K2=11,K3=34,north=96,east=96,
            hdir=1,hphase=0,vdir=1,vphase=PI/12)

    c2=Heart(layer=layer_2,K1=11,K2=6,K3=34, north=96,east=96,
            hdir=-1,hphase=0,vdir=1,vphase=PI)
    mc2=Heart_Mechanics(layer=layer_m2,K1=11,K2=6,K3=34, north=96,east=96,
            hdir=-1,hphase=0,vdir=1,vphase=PI)

    c2a=Heart(layer=layer_2a,K1=11,K2=6,K3=34, north=96,east=96,
            hdir=-1,hphase=0,vdir=1,vphase=PI)
    mc2a=Heart_Mechanics(layer=layer_m2a,K1=11,K2=6,K3=34, north=96,east=96,
            hdir=-1,hphase=0,vdir=1,vphase=PI)

    c2b=Heart(layer=layer_2b,K1=11,K2=6,K3=34, north=96,east=96,
            hdir=-1,hphase=0,vdir=1,vphase=PI)
    mc2b=Heart_Mechanics(layer=layer_m2b,K1=11,K2=6,K3=34, north=96,east=96,
            hdir=-1,hphase=0,vdir=1,vphase=PI)

    c2c=Heart(layer=layer_2c,K1=11,K2=6,K3=34, north=96,east=96,
            hdir=-1,hphase=0,vdir=1,vphase=PI)
    mc2c=Heart_Mechanics(layer=layer_m2c,K1=11,K2=6,K3=34, north=96,east=96,
            hdir=-1,hphase=0,vdir=1,vphase=PI)


    # canvas-------------------------------------------------------------------
    canvas.target_scale=50
    pyglet.app.run()

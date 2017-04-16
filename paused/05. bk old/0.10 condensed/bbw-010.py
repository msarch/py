#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what :  simple pyglet anim

# kbw r1.0

##  IMPORTS -------------------------------------------------------------------

from pyglet import clock
from random import choice
import pyglet
from pyglet.gl import *
from pyglet.window import key

##  CONSTANTS AND VARIABLES ---------------------------------------------------
fps = 25.0                  # windows refresh rate
n = 0
grobs = []                    #list of all groms created
actors1 = []
actors2 = []
tintors1=[]
tintors2=[]
hfac=-2.0
vfac=-1.5
kapla_colors = ((1.00, 0.84, 0.00),(0.00, 0.39, 0.00), (0.00, 0.39, 0.00),\
        (1.00, 0.27, 0.00), (0.00, 0.00, 0.55))
##  CANVAS --------------------------------------------------------------------
class Canvas(pyglet.window.Window): # parts from langton ants

    def __init__(self,fps):

        pyglet.window.Window.__init__(self,fullscreen=True)
        self.set_mouse_visible(False)
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        self.screen_width = screen.width
        self.screen_height = screen.height
        self.cx = (self.width*0.5)+1
        self.cy = (self.height*0.5)+1
        self.fps=fps
        glClearColor(0.0, 0.0, 0.0, 0.0) # set background color to black
        #glClearColor(1.0, 1.0, 1.0, 1.0) # set background color to white
        glLoadIdentity() # reset transformation matrix
        glTranslatef(self.cx,self.cy,0.0)   # Move Origin to screen center

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            exit()

    def on_draw(self):
        global grobs
        self.clear()                      # clear graphics
        for grob in grobs:
            grob.pygdraw()              # --- PYGLET OUTPUT
            #obgeom.pdfy()              # --- PDF OUTPUT
            #obgeom.dxfy()              # --- DXF OUTPUT
            #obgeom.rhinofy()           # --- RHINO OUTPUT
            #obgeom.imagify()           # --- IMAGE OUTPUT

##  TRANSFORMATION MATRIX -----------------------------------------------------

def id_matrix():
    return ([1, 0, 0, 0, 1, 0, 0, 0, 1])

def tm(dx, dy): # Returns the transformation matrix for a (dx,dy) translation.
    return ([1, 0, dx, 0, 1, dy, 0, 0 ,1])

def xsm():#transformation matrix for the symmetry through x axis
    return([1, 0, 0, 0, -1, 0, 0, 0, 1])

def ysm():# transformation matrix for the symmetry through y axis
    return([-1, 0, 0, 0, 1, 0, 0, 0, 1])


##--- SIMPLE RECTANGLE (ortho) ------------------------------------------------

class Rect(object):
    """ rectangle is defined by center x,y and size w,h
    """
    def __init__(self, width=300, height=100, xc=0, yc=0, \
                 color=(0,0,0), M=id_matrix()):
        # self vertex list:
        #                             centroid,     [0]
        #                             bottom left,  [1]
        #                             bottom right, [2]
        #                             top right,    [3]
        #                             top left      [4]
        self.v=[[xc,yc],[xc-width*0.5,yc-height*0.5],\
                        [xc+width*0.5,yc-height*0.5],\
                        [xc+width*0.5,yc+height*0.5],\
                        [xc-width*0.5,yc+height*0.5],]
        self.M = M
        self.width=width
        self.height=height
        self.color = color
        grobs.append(self)

    @property
    def type(self):
        return (self.__class__)

    @property
    def M(self):
        return (self._M)

    @M.setter
    def M(self,matrix):
        self._M = matrix

    @property
    def color(self):
        return (self._color)

    @color.setter
    def color(self,c):
        self._color = c

    def once_transform(self,M):
        """ applies the PROVIDED matrix M transformation to all vertex.
        """
        for index, vtx in enumerate(self.v):
            self.v[index] = [M[0]*vtx[0]+M[1]*vtx[1]+M[2],\
                             M[3]*vtx[0]+M[4]*vtx[1]+M[5]]

    def transform(self):
        """ applies OWN's CURRENT matrix transformation
        to all transformable vertex, incl the centroid.
        """
        for index, vtx in enumerate(self.v):
            self.v[index] = [self.M[0]*vtx[0]+self.M[1]*vtx[1]+self.M[2],\
                             self.M[3]*vtx[0]+self.M[4]*vtx[1]+self.M[5]]

    def __repr__(self):
       return "Rec\tw,h:(%.1dx%.1d), @(%.1d,%1d), \t\tM%3s" \
       % (self.width(), self.height(), self.v[0][0], self.v[0][1], self.M)

    def copy(self):
        rect=Rect(self.width,self.height,self.v[0][0],self.v[0][1],self.color,self.M)
        return rect

    def pygdraw(self, **kwargs):
        """ Draws the rectangle with the bottom left corner at x, y.
        The current stroke, strokewidth and fill color are applied.
        """
        pyglet.gl.glColor3f(self.color[0],self.color[1],self.color[2])
        glBegin(GL_QUADS)
        glVertex3f(self.v[1][0], self.v[1][1], 0.0)  # bottom left
        glVertex3f(self.v[2][0], self.v[2][1], 0.0)  # bottom right
        glVertex3f(self.v[3][0], self.v[3][1], 0.0)  # top right
        glVertex3f(self.v[4][0], self.v[4][1], 0.0)  # top left
        glEnd()


##  DRAWING BEGINS HERE -------------------------------------------------------

def scene_setup():

# GROBS LIST ------------------------------------------------------------------
    e=6*g
    w=11*g
    h=33*g

    r1 = Rect(h, e,-w/2-h/2-e,e/2+w/2,(choice(kapla_colors)))
    r2 = r1.copy()
    r2.once_transform(xsm())
    r3 = r1.copy()
    r3.once_transform(ysm())
    r4 = r3.copy()
    r4.once_transform(xsm())
    r5 = Rect(e,h,-w/2-e/2,w/2+e+h/2,(choice(kapla_colors)))
    r6 = r5.copy()
    r6.once_transform(ysm())
    r7 = r5.copy()
    r7.once_transform(xsm())
    r8 = r7.copy()
    r8.once_transform(ysm())

    m=tm(19,0)
    h_slider = Rect(h,w,0,0,(choice(kapla_colors)),m)

    m=tm(0,7)
    v_slider = Rect(w,h,0,0,(choice(kapla_colors)),m)

# SCHEDULED ACTIONS LIST ------------------------------------------------------

    actors1.extend([h_slider]) #.extend: add multiple elements,.append: add one
    actors2.extend([v_slider]) #.extend: add multiple elements,.append: add one

    tintors1.extend([r1,r4,r8,r5])
    tintors2.extend([r1,r4,r6,r7])

def actors1_update(dt):
    global actors1,hfac
    for a in actors1 :
        a.transform()
        if (a.v[1][0]<cl or a.v[2][0]>cr):  # if bounce,
           # a.M[2] *=-1                         # reverse dir
            a.color = choice(kapla_colors)      # change clr
            a.M[2] *= hfac                         # change speed
            hfac=1.0/hfac
            for t in tintors1 : t.color = (choice(kapla_colors))

def actors2_update(dt):
    global actors2,vfac
    for a in actors2 :
        a.transform()
        if (a.v[4][1]>ct or a.v[1][1]<cb):  # if bounce,
            #a.M[5] *=-1                         # reverse dir
            a.color = choice(kapla_colors)      # change clr
            a.M[5] *= vfac                         # change speed
            vfac=1.0/vfac
            for t in tintors2 : t.color = (choice(kapla_colors))


def image_capture(dt):
    global n
    n+=1
    file_num=str(n).zfill(5)
    filename="fr-"+file_num+'.png'
    pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
    if n>300: exit()
##  MAIN ----------------------------------------------------------------------
def main():
    c = Canvas(fps)        # standard fullscreen window

    global g
    g=int(c.screen_height/85)  # grid cell size, used to size object relatively
    global cw,ch
    cw,ch =c.width,c.height
    global cl,cr,ct,cb
    cl,cr,ct,cb=-cw*0.5,cw*0.5,ch*0.5,-ch*0.5

    clock.schedule_interval(actors1_update, 1.0/fps)
    clock.schedule_interval(actors2_update, 1.0/fps)
    #clock.schedule_interval(image_capture, 5/fps) #uncomment to capture img
    #clock.schedule_interval(c.draw, 1.0/fps)

    scene_setup()
    pyglet.app.run()

##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()

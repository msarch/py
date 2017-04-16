#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : main pyglet loop

# r0.7

##--- IMPORTS -----------------------------------------------------------------
import pyglet
from pyglet.gl import *
from pyglet import window
from pyglet.window import key

import toxy
from greom import Point, SimpleLine, SimpleRec
from toxy import *


##--- CONSTANTS ---------------------------------------------------------------

frames_per_sec=25.0
debug=1
population=[]
actors=[]

# Grid stuff
grid_size=10
platform = pyglet.window.get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()
grid_columns = screen.width / grid_size
grid_rows = screen.height / grid_size
grid_on=1
##--- CANVAS CLASS ------------------------------------------------------------

class Canvas(pyglet.window.Window):
    
    def __init__(self):

        window.Window.__init__(self,fullscreen=True)

        glShadeModel(GL_SMOOTH)    # Enables smooth shading
        glClearColor(0.0, 0.0, 0.0, 0.0) # set background color to black
        glLoadIdentity() # reset transformation matrix
        # glClearDepth(1.0)        # Depth buffer setup
        # glEnable(GL_DEPTH_TEST)        # Enables depth testing
        # glDepthFunc(GL_LEQUAL)        # The type of depth test to do
        # glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        # Really nice perspective calculations
        
    def on_key_press(self, symbol, modifiers):
            if symbol == key.ESCAPE:
                exit()
                
    def on_mouse_press(self,x,y,button,modifiers):
        pass
        
    def grid_draw(self, **kwargs):
        """ Draws the grid, color grey.
        """
        pyglet.gl.glColor4f(0.23,0.23,0.23,1.0) # gray
        # Horizontal lines
        for i in range(grid_rows):
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (0, i * grid_size, screen.width, i * grid_size)))
        # Vertical lines
        for j in range(grid_columns):
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (j * grid_size, 0, j * grid_size, screen.height)))

    def draw(self,dt):
        self.clear()                    # clear graphics
        #if grid_on: self.grid_draw() 
        # pyglet.gl.glColor4f(0.23,0.23,0.23,1.0) # gray
        print 'running draw'
        print 'FPS is %f' % pyglet.clock.get_fps()  
        pyglet.gl.glColor3f(0.5, 0.5, 1.0)    # set the color to sky-blue 
        for lmnt in population:
            lmnt.pygdraw()              # --- PYGLET OUTPUT
            if debug :
                print(lmnt)             # --- TEXT OUTPUT
            #obgeom.pdfy()              # --- PDF OUTPUT
            #obgeom.dxfy()              # --- DXF OUTPUT
            #obgeom.rhinofy()           # --- RHINO OUTPUT
            #obgeom.imagify()           # --- IMAGE OUTPUT

        return pyglet.event.EVENT_HANDLED


##--- DRAWING_LIST CLASS ------------------------------------------------------

class DrawingList(list):
    
    def __init__(self):
        
        
        pass

##--- SPECIFIC DRAWING HERE ---------------------------------------------------


def actors_update(dt): #dt is defined in 
    print 'running actors1update'
    m=toxy.tm(10,0)
    for actor in actors:
            actor.operate(m)
        

def actors2_update(dt): #dt is defined in 
    print 'running actors2 update'
    pass
            
 
def list_init():
    print 'running do_init'
    a = Point(10,100)
    line1 = SimpleLine(10,10,10,180)   # startpoint, endpoint
    rec1 = SimpleRec(10,180,20,300)    # basepoint, width, height
    rec2 = rec1.copy()
     
    population.append(a)
    population.append(line1)
    population.append(rec1)
    population.append(rec2)
    actors.append(rec2)

    for lmnt in population:
       print lmnt
       
##--- SPECIFIC DRAWING HERE ---------------------------------------------------



    
##--- MAIN --------------------------------------------------------------------

if __name__ == "__main__":
    
    list_init()
    c = Canvas()
    pyglet.clock.schedule_interval(c.draw, 1.0/frames_per_sec)
    pyglet.clock.schedule_interval(actors_update, 1.0/8)
    pyglet.clock.schedule_interval(actors2_update, 50.0/frames_per_sec)

    pyglet.app.run()
        

##------------------------------------------------------------------------------

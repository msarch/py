#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : main pyglet loop

# r0.8

##  IMPORTS -----------------------------------------------------------------

import pyglet
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key
from grobs import *


##  CONSTANTS AND VARIABLES ---------------------------------------------------

actors1=[]
tintors1=[]
tintors2=[]
tintors3=[]

##  CANVAS --------------------------------------------------------------------
class Canvas(pyglet.window.Window): # parts from langton ants

    def __init__(self,fps):

        pyglet.window.Window.__init__(self,fullscreen=True)

        # Initialize screen resolution
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        self.screen_width = screen.width
        self.screen_height = screen.height
        self.cx = (self.width/2)+1
        self.cy = (self.height/2)+1
        self.fps=fps

        self.frame_counter = 0
        glClearColor(0.0, 0.0, 0.0, 0.0) # set background color to black
        glLoadIdentity() # reset transformation matrix
        glTranslatef(self.cx,self.cy,0.0)   # Move Origin to screen center
        # glClearDepth(1.0)        # Depth buffer setup
        # glEnable(GL_DEPTH_TEST)        # Enables depth testing
        # glDepthFunc(GL_LEQUAL)        # The type of depth test to do
        # glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST) # nice perspectives
        # glShadeModel(GL_SMOOTH)    # Enables smooth shading

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            exit()

    def on_mouse_press(self,x,y,button,modifiers):
        print x,y
        exit()

    def draw(self,dt):
        global grobs
        self.clear()                      # clear graphics
        self.frame_counter += 1
        print '\nframe %d -----------%f\n' \
              %(self.frame_counter, pyglet.clock.get_fps())
        c=(0.5, 0.5, 1.0)
        pyglet.gl.glColor3f(c[0],c[1],c[2])    # set the color to sky-blue

        for grob in grobs:
            grob.pygdraw()              # --- PYGLET OUTPUT
            print(grob)                 # --- TEXT OUTPUT
            #obgeom.pdfy()              # --- PDF OUTPUT
            #obgeom.dxfy()              # --- DXF OUTPUT
            #obgeom.rhinofy()           # --- RHINO OUTPUT
            #obgeom.imagify()           # --- IMAGE OUTPUT

    def run(self):
        pyglet.clock.schedule_interval(self.draw, 1.0/self.fps)
        pyglet.app.run()

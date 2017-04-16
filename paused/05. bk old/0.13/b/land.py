#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: land :: rev 13-a :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------

import pyglet
from pyglet.gl import *
from pyglet.window import key
from zulus import Zulu
from rules import Rule

##  CONSTANTS AND VARIABLES ---------------------------------------------------
##  CLASSES -------------------------------------------------------------------


class Zululand(pyglet.window.Window):

    def __init__(self):
        pyglet.window.Window.__init__(self,fullscreen=True)
        self.set_mouse_visible(False)
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        self.xmin=-screen.width*0.5
        self.xmax=screen.width*0.5
        self.ymin=-screen.height*0.5
        self.ymax= screen.height*0.5


        glClearColor(0.0, 0.0, 0.0, 0.0) # set background color to black
        #glClearColor(1.0, 1.0, 1.0, 1.0) # set background color to white
        glLoadIdentity() # reset transformation matrix
        glTranslatef((screen.width*0.5)+1,(screen.height*0.5)+1,0)  # Move Origin to screen center

        # schedule the update function, 60 times per second
        pyglet.clock.schedule_interval(self.update, 1.0/120.0)


    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:exit()

    def on_draw(self):
        """Clear the current OpenGL context, reset the model/view matrix and
        invoke the `draw()` methods of the renderers in order
        """
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glClear(GL_STENCIL_BUFFER_BIT)

        for z in Zulu.nation:
            z.draw()

    def get_boundaries(self):
        self.boundaries=(self.xmin,self.ymin,self.xmax,self.ymax)
        return self.boundaries

    def run(self):
        """ Opens the application windows and starts drawing the canvas.
        """
        pyglet.app.run()

    def update(self,dt):
        for r in Rule.book:
            r.update(dt)



#--- FUNCTIONS ----------------------------------------------------------------



#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: display :: rev 13-c :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------

import pyglet
import zululand
from pyglet.gl import *
from pyglet.window import key


##  CONSTANTS AND VARIABLES ---------------------------------------------------

##  CLASS PYGLET ------------------------------------------------------------------

class Window(pyglet.window.Window):

    def __init__(self,land):
        pyglet.window.Window.__init__(self,fullscreen=True)
        self.set_mouse_visible(False)
        _size=get_size()
        self.land=land
        self.xc = (self.land.size[0]*0.5)+1
        self.yc = (self.land.size[1]*0.5)+1
        print 'center of display =', self.xc,self.yc
        # set background color
        glClearColor(self.land.color[0],self.land.color[1],\
                self.land.color[2],self.land.color[3])
        #glClearColor(1.0, 1.0, 1.0, 1.0) # set background color to white
        glLoadIdentity() # reset transformation matrix
        glTranslatef(self.xc,self.yc,0.0)   # Move Origin to screen center

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:exit()

    def on_draw(self):
        """Clear the current OpenGL context, reset the model/view matrix and
        invoke the `draw()` methods of the renderers in order
        """
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glClear(GL_STENCIL_BUFFER_BIT)
        glLoadIdentity()
        #
        self.land.draw()
        print 'drawing'
#--- FUNCTIONS ----------------------------------------------------------------
def get_size():
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screen = display.get_default_screen()
    xmax = screen.width
    ymax = screen.height
    return(xmax,ymax)







#!/usr/bin/python
# -*- coding: utf-8 -*-

# msarch@free.fr * feb 2015 * bw-rev116

##--- IMPORTS -----------------------------------------------------------------
from pyglet.app import run
from pyglet.clock import schedule_interval
from pyglet.gl import glClear, glLoadIdentity, glTranslatef
from pyglet.gl import GL_COLOR_BUFFER_BIT, \
                    GL_DEPTH_BUFFER_BIT, \
                    GL_STENCIL_BUFFER_BIT
from pyglet.window import Window
from bw.display import CENTX,CENTY
from bw.shape import Shape 

import pyglet
#--- PYGLET Window setup ------------------------------------------------------
WIN = Window(fullscreen=True)
glLoadIdentity()
glTranslatef(CENTX, CENTY, 0)

@WIN.event
def on_draw():  # pyglet window draw event
    glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_STENCIL_BUFFER_BIT)
    print 
    print ':: D(',
    Shape.draw()

def tick(dt):
    print
    print  ':: T(',
      
##--- MAIN --------------------------------------------------------------------
def start():
    print ':: starting pyglet loop'
    schedule_interval(tick, 1.0/60)   # infinite loop
    pyglet.app.run()

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * nov 2014 * bw-rev111b
pyglet engine loop : calls groups paint, calls rules updates
'''
##---IMPORTS ------------------------------------------------------------------
import pyglet
from pyglet.gl import *
from utils.cfg import WIDTH, HEIGHT, CENTX, CENTY, FRAMERATE  # constants
from rules import rules
from shapes import shapes

#--- GLOBALS ------------------------------------------------------------------
paused = False
show_fps = False
fullscr = True

#--- PYGLET Window setup ------------------------------------------------------
VIEW = pyglet.window.Window(resizable=True)
VIEW.set_fullscreen(fullscr)
VIEW.set_mouse_visible(False)
# next 2 lines enable depth
glEnable(GL_DEPTH_TEST)
glDepthMask(GL_TRUE)
glOrtho(-CENTX, CENTX, -CENTY, CENTY, 0.1, 1)  # dont understand, check this  # TODO
# next 2 lines enable transparency
glEnable (GL_BLEND)
glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
# glClear(GL_DEPTH_BUFFER_BIT) only works when glDepthMask(GL_TRUE) was called before. Otherwise, the depth buffer is not writeable.
glClear(GL_COLOR_BUFFER_BIT)
glClear(GL_DEPTH_BUFFER_BIT)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glTranslatef(CENTX, CENTY, 0)
CLOCKDISPLAY = pyglet.clock.ClockDisplay()
try:
    # Try and create a window config with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True)
except pyglet.window.NoSuchConfigException:
    print "Smooth contex could not be aquiried."


#--- VIEW key handling --------------------------------------------------------
@VIEW.event
def on_key_press(symbol, modifiers):  # pyglet window's key event
    global paused, show_fps, fullscr
    if symbol == pyglet.window.key.ESCAPE:
        exit(0)
    elif symbol == pyglet.window.key.SPACE:
        paused = (True,False)[paused]
    else:
        show_fps = (True,False)[show_fps]


#--- PYGLET ENGINE ------------------------------------------------------------
@VIEW.event
def on_draw():  # pyglet window draw event
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shapes.paint()
    # inserer ICI? le facteur d'adaptation a la taille de l'ecran (camera?)    # TODO
    # how to render bigger than screen to file with resize for display         # TODO
    if show_fps:
        CLOCKDISPLAY.draw()


#--- scene update -------------------------------------------------------------
def tick(dt):
    if paused:
        pass
    else:
        rules.tick(dt)

#--- run mode options 1 : fullscreen animation --------------------------------
def start():
    print '::'
    print '::                          :           :           :'
    print '::                          :::         :::         :::'
    print '::                          :::::       :::::       :::::'
    print ':: starting field engine    :::::::     :::::::     :::::::'
    print '::                          :::::       :::::       :::::'
    print '::                          :::         :::         :::'
    print '::                          :           :           :'
    print '::'

    pyglet.clock.schedule_interval(tick, FRAMERATE)   # infinite loop
    pyglet.app.run()

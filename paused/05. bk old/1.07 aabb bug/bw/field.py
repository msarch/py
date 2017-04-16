#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev107
pyglet engine : calls actors paint, calls rules updates
'''
##---IMPORTS ------------------------------------------------------------------
import pyglet
from pyglet.gl import *
from utils.cfg import WIDTH, HEIGHT, CENTX, CENTY, FRAMERATE  # constants
import rules
import actors

#--- GLOBALS ------------------------------------------------------------------
paused = False
show_fps = False
fullscr = True

#--- PYGLET Window setup ------------------------------------------------------
VIEW = pyglet.window.Window(resizable=True)
VIEW.set_fullscreen(fullscr)
VIEW.set_mouse_visible(False)
glMatrixMode(GL_PROJECTION)
glMatrixMode(GL_MODELVIEW)
gluOrtho2D(0, WIDTH, 0, HEIGHT)  # dont understand, check this                 # TODO
glLoadIdentity()
glTranslatef(CENTX, CENTY, 0)
glClear(GL_COLOR_BUFFER_BIT)
CLOCKDISPLAY = pyglet.clock.ClockDisplay()


#--- VIEW key handling --------------------------------------------------------
@VIEW.event
def on_key_press(symbol, modifiers):  # pyglet window's key event
    global paused, show_fps, fullscr
    if symbol == pyglet.window.key.ESCAPE:
        exit(0)
    elif symbol == pyglet.window.key.F:
        fullscr = (True,False)[fullscr]  # resizable or zoom in/out            # TODO
        VIEW.set_fullscreen(fullscr)
    elif symbol == pyglet.window.key.SPACE:
        paused = (True,False)[paused]
    else:
        show_fps = (True,False)[show_fps]


#--- PYGLET ENGINE ------------------------------------------------------------
@VIEW.event
def on_draw():  # pyglet window draw event
    glClear(GL_COLOR_BUFFER_BIT)
    actors.paint()
    # inserer ICI? le facteur d'adaptation a la taille de l'ecran              # TODO
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
    print ''
    print ':: starting field engine...'
    pyglet.clock.schedule_interval(tick, FRAMERATE)   # infinite loop
    pyglet.app.run()

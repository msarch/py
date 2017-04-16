#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev106

this is the pyglet engine.
- displays cells on windows redraws
- cycle through rules at each clock tick
'''

##---IMPORTS ------------------------------------------------------------------
import pyglet.gl
from pyglet.gl import *
from pyglet.clock import ClockDisplay, schedule_interval
from pyglet.window import key
from pyglet.gl import(
        glLoadIdentity,
        glMatrixMode,
        gluOrtho2D,
        GL_MODELVIEW, GL_PROJECTION,
        )
from utils.cfg import WIDTH, HEIGHT, CENTX, CENTY  # constants

import rules
import cells

#--- CONSTANTS ----------------------------------------------------------------
FRAMERATE = 1.0/60
MOVIE_FRAMERATE = 1.0 / 25  # framerate for movie export
CLOCKDISPLAY = ClockDisplay()

# how to render bigger than screen to file with resize for display                # TODO
#--- GLOBALS ------------------------------------------------------------------
paused = False
show_fps = False
fullscr = True

#--- PYGLET Window setup ------------------------------------------------------
VIEW = pyglet.window.Window(resizable=True)
VIEW.set_fullscreen(fullscr)
VIEW.set_mouse_visible(False)

def gl_setup():  # general GL setup
    glMatrixMode(GL_PROJECTION)
    glMatrixMode(GL_MODELVIEW)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)  # dont understand, check this                # TODO
    glLoadIdentity()
    glTranslatef(CENTX, CENTY, 0)
    glClear(GL_COLOR_BUFFER_BIT)

#--- VIEW key handling --------------------------------------------------------
@VIEW.event
def on_key_press(symbol, modifiers):  # pyglet window's key event
    global paused, show_fps, fullscr
    if symbol == key.ESCAPE:
        exit(0)
    elif symbol == key.F:
        fullscr = (True,False)[fullscr]  # resizable                        # TODO
        VIEW.set_fullscreen(fullscr)
    else:
        paused = (True,False)[paused]
        show_fps = (True,False)[show_fps]

#--- PYGLET ENGINE ------------------------------------------------------------
@VIEW.event
def on_draw():  # pyglet window draw event
    glClear(GL_COLOR_BUFFER_BIT)
    # inserer ICI? le facteur d'adaptation a la taille de l'ecran           # TODO
    cells.paint()

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
    print''
    print 'starting field engine...'
    gl_setup()
    schedule_interval(tick, FRAMERATE)   # infinite loop
    pyglet.app.run()

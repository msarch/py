#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev105

this is the pyglet engine.
- displays cells on windows redraws
- cycle through rules at each clock tick
'''

##---IMPORTS ------------------------------------------------------------------
from   itertools import izip
from   pyglet import clock
import pyglet.gl
from   pyglet.gl import *
from   pyglet.window import key, get_platform
from   pyglet.gl import(
        glLoadIdentity,
        glMatrixMode,
        gluOrtho2D,
        GL_MODELVIEW, GL_PROJECTION,
        )
from   colors import *
from   shapes import *
from   rules import *

#--- CONSTANTS ----------------------------------------------------------------
FRAMERATE = 1.0/30
MOVIE_FRAMERATE = 1.0 / 25  # framerate for movie export
CLOCKDISPLAY = clock.ClockDisplay()
_screen = get_platform().get_default_display().get_default_screen()
WIDTH, HEIGHT = _screen.width*1.0 ,_screen.height*1.0
CENTX, CENTY = WIDTH*0.5, HEIGHT*0.5
SCREEN = AABB(-CENTX, -CENTY, CENTX, CENTY)
ASPECT = WIDTH / HEIGHT

# @TODO : check how to go bigger than screen, then resize to fullscreen
#--- GLOBALS ------------------------------------------------------------------
paused = False
show_fps = True
fullscreen = True
field_color = white

#--- PYGLET Window setup ------------------------------------------------------
VIEW = pyglet.window.Window(resizable = True)
VIEW.set_fullscreen(fullscreen)
VIEW.set_mouse_visible(not fullscreen)

def set_field_color(new_color):  # change background color
    global field_color
    field_color = new_color
    glClearColor(new_color.r,new_color.g,new_color.b,new_color.a)

def view_setup():  # general GL setup
    glMatrixMode(GL_PROJECTION)
    glMatrixMode(GL_MODELVIEW)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glLoadIdentity()
    glTranslatef(CENTX, CENTY, 0)

#--- VIEW key handling --------------------------------------------------------
@VIEW.event
def on_key_press(symbol, modifiers):  # override pyglet window's
    global paused, show_fps, fullscreen
    if symbol == key.ESCAPE:
        exit(0)
    elif symbol == key.F:
        fullscreen = (True,False)[fullscreen]
        print fullscreen
        VIEW.set_fullscreen(fullscreen)
        VIEW.set_mouse_visible(not fullscreen)
    else:
        paused = (True,False)[paused]
        show_fps = (True,False)[show_fps]

#--- PYGLET ENGINE ------------------------------------------------------------
@VIEW.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    # @TODO : inserer le facteur d'adaptation a la taille de l'ecran,
    for shp in setup:
        if shp.peg:
            shp.paint(shp.peg)
        else:
            pass

    if show_fps:
        CLOCKDISPLAY.draw()

#--- scene update -------------------------------------------------------------
def tick(dt):
    if paused:
        pass
    else:
        for rule in ruleset:
            rule.tick(dt)

#--- run mode options 1 : fullscreen animation --------------------------------
def animate():
    set_field_color(field_color)
    view_setup()
    clock.schedule_interval(tick, FRAMERATE)   # infinite loop ------------
    pyglet.app.run()

#--- NOTES --------------------------------------------------------------------
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
'''

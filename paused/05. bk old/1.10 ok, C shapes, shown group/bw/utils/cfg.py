#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev106
'''
#--- Imports ------------------------------------------------------------------
from collections import namedtuple
from   pyglet.window import get_platform
from   pyglet.gl import *

#--- VARS ---------------------------------------------------------------------


#--- CONSTANTS ----------------------------------------------------------------
FRAMERATE = 1.0/60

#--- CONSTANTS ----------------------------------------------------------------
Peg = namedtuple('Peg','x y angle')
Vel = namedtuple('Vel','vx vy av')
Vel2 = namedtuple('Speed1', 'speed heading')
Vel3 = namedtuple('Speed2', 'x y angle speed')
Vel4 = namedtuple('Peg2', 'speed head_to') # or use Peg3 ??
Vel5 = namedtuple('Peg3', 'speed path') # target

Point  = namedtuple('Point', 'x y')
AABB = namedtuple('AABB', 'lox loy hix hiy')

ORIGIN = Point(0.0, 0.0)
IDLE   = Vel(0.0, 0.0, 0.0)
DOCKED = Peg(0.0, 0.0, 0.0)

#--- DISPLAY INFO -------------------------------------------------------------
_screen = get_platform().get_default_display().get_default_screen()
WIDTH, HEIGHT = _screen.width*1.0 ,_screen.height*1.0
ASPECT = WIDTH / HEIGHT
CENTX, CENTY = WIDTH*0.5, HEIGHT*0.5
SCREEN = AABB(-CENTX, -CENTY, CENTX, CENTY)

#--- COLORS -------------------------------------------------------------------
Color = namedtuple('Color', 'r g b a')

orange  = Color(255, 127,   0,   0)
white   = Color(255, 255, 255,   0)
black   = Color(  0,   0,   0,   0)
yellow  = Color(255, 255,   0,   0)
red     = Color(200,   0,   0,   0)
blue    = Color(127, 127, 255,   0)
blue50  = Color(127, 127, 255, 127)
pink    = Color(255, 187, 187,   0)
very_light_grey = Color(242, 242, 242, 0)
kapla_colors = (
            Color(255, 214,  0,   0),
            Color(  0, 99,   0,   0),
            Color(255, 69,   0,   0),
            Color(  0,  0, 140,   0)
            )

def background_color(color=white):
    glClearColor(*color)

def any():
    # TODO yeld a random color
    pass

def any_kapla():
    # TODO yeld a random color from kapla
    pass





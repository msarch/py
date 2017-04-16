#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * nov 2014 * bw-rev112
'''
#--- Imports ------------------------------------------------------------------
from collections import namedtuple
from   pyglet.window import get_platform
from   pyglet.gl import *

#--- VARS ---------------------------------------------------------------------


#--- CONSTANTS ----------------------------------------------------------------
FRAMERATE = 1.0/60
EPSILON = 1e-5

#--- CONSTANTS ----------------------------------------------------------------
Peg = namedtuple('Peg','x y z angle')
Vel = namedtuple('Vel','vx vy av')
Vel2 = namedtuple('Speed1', 'speed heading')
Vel3 = namedtuple('Speed2', 'x y angle speed')
Vel4 = namedtuple('Peg2', 'speed head_to') # or use Peg3 ??
Vel5 = namedtuple('Peg3', 'speed path') # target

Point  = namedtuple('Point', 'x y')
AABB = namedtuple('AABB', 'lox loy hix hiy')

ORIGIN = Point(0.0, 0.0)
IDLE   = Vel(0.0, 0.0, 0.0)
DOCKED = Peg(0.0, 0.0, 0.0, 0.0)
BACK = Peg(0.0, 0.0, -0.8, 0.0)


#--- DISPLAY INFO -------------------------------------------------------------
_screen = get_platform().get_default_display().get_default_screen()
WIDTH, HEIGHT = _screen.width*1.0 ,_screen.height*1.0
ASPECT = WIDTH / HEIGHT
CENTX, CENTY = WIDTH*0.5, HEIGHT*0.5
SCREEN = AABB(-CENTX, -CENTY, CENTX, CENTY)

##---TRANSFORMATION MATRIXES---------------------------------------------------
MAT_id = [1, 0, 0, 0, 1, 0, 0, 0, 1]  # Identity matrix
MAT_X_flip = [1, 0, 0, 0, -1, 0, 0, 0, 1]  # X axi symetry matrix
MAT_Y_flip = [-1, 0, 0, 0, 1, 0, 0, 0, 1]  # Y axi symetry matrix

#--- COLORS -------------------------------------------------------------------
Color = namedtuple('Color', 'r g b a')

orange  = Color(255, 127,   0, 255)
white   = Color(255, 255, 255, 255)
black   = Color(  0,   0,   0, 255)
yellow  = Color(255, 255,   0, 255)
red     = Color(255,   0,   0, 255)
blue    = Color(127, 127, 255, 255)
blue50  = Color(127, 127, 255, 127)
pink    = Color(255, 187, 187, 255)
very_light_grey = Color(242, 242, 242, 0)

# kapla_colors
r_k = Color(255, 69,   0,   255)  # red kapla
b_k = Color(  0,  0, 140,   255)  # blue kapla
g_k = Color(  0, 99,   0,   255)  # green kapla
y_k = Color(255, 214,  0,   255)  # yellow kapla
kapla_colors=(r_k, g_k, b_k, y_k, b_k)  # addded 1 color for pb  w 4 kaplas     TODO

def set_background_color(color=white):
    glClearColor(*blue)

def any():
    # TODO yeld a random color
    pass


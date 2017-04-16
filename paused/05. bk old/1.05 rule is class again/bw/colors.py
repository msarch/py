#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev105
'''
#--- Imports ------------------------------------------------------------------
from collections import namedtuple


#--- COLORS -------------------------------------------------------------------
Color = namedtuple('Color', 'r g b a')

orange  = Color(255, 127,   0,   0)
white   = Color(255, 255, 255,   0)
black   = Color(  0,   0,   0,   0)
yellow  = Color(255, 255,   0,   0)
red     = Color(200,   0,   0,   0)
blue    = Color(127, 127, 255,   0)
pink    = Color(255, 187, 187,   0)
very_light_grey = Color(242, 242, 242, 0)
kapla_colors = (
            Color(255, 214,  0,   0),
            Color(  0, 99,   0,   0),
            Color(  0, 99,   0,   0),
            Color(255, 69,   0,   0),
            Color(  0,  0, 140,   0)
            )

def any():
    # TODO yeld a random color
    pass

def any_kapla():
    # TODO yeld a random color from kapla
    pass





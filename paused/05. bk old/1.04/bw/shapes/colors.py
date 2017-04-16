#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * july 2014 * bw-rev103
'''
from pyglet.gl import *

##---COLOR CLASS---------------------------------------------------------------
class Color(object):
    orange  = (255, 127, 0)
    white   = (255, 255, 255)
    black   = (0, 0, 0)
    yellow  = (255, 255, 0)
    red     = (200, 0, 0)
    blue    = (127, 127, 255)
    pink    = (255, 187, 187)
    very_light_grey = (0.95, 0.95, 0.95, 0)
    kapla_colors = (
            (1.00, 0.84, 0.00),
            (0.00, 0.39, 0.00),
            (0.00, 0.39, 0.00),
            (1.00, 0.27, 0.00),
            (0.00, 0.00, 0.55)
            )

    def any():
        # TODO yeld a random color
        pass

    def any_kapla():
        # TODO yeld a random color from kapla
        pass

def set_background(color):
    glClearColor(color[0]/255.00, color[0]/255.00, color[0]/255.00, 0.00)



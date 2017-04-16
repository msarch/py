#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * jan 2015 * bw-rev113
adapted from Jonathan Hartley's code
'''

#--- IMPORTS ------------------------------------------------------------------
from utils.color import *  # all colors
from pyglet.gl import GL_TRIANGLE_STRIP, GL_LINE_STRIP
from engine.shape import Shape
#--- COLOR PLANE --------------------------------------------------------------
# Not part of the standard API but too convenient to leave out.

def Colorplane(x, y, width, height, *a):  #                                   # TODO
    '''
    Draws a rectangle that emits a different fill color from each corner.
    An optional number of colors can be given:
        - four colors define top left, top right, bottom right and bottom left,
        - three colors define top left, top right and bottom,
        - two colors define top and bottom,
        - no colors assumes black top and white bottom gradient.
        from Tom De Smedt, Frederik De Bleser NodeBox API
    '''
    if len(a) == 2:
        # Top and bottom colors.
        clr1, clr2, clr3, clr4 = a[0], a[0], a[1], a[1]
    elif len(a) == 4:
        # Top left, top right, bottom right, bottom left.
        clr1, clr2, clr3, clr4 = a[0], a[1], a[2], a[3]
    elif len(a) == 3:
        # Top left, top right, bottom.
        clr1, clr2, clr3, clr4 = a[0], a[1], a[2], a[2]
    elif len(a) == 0:
        # Black top, white bottom.
        clr1 = clr2 = (0,0,0,1)
        clr3 = clr4 = (1,1,1,1)
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(width, height, 1)
    glBegin(GL_QUADS)
    glColor4f(clr1[0], clr1[1], clr1[2], clr1[3] * _alpha); glVertex2f(-0.0,  1.0)
    glColor4f(clr2[0], clr2[1], clr2[2], clr2[3] * _alpha); glVertex2f( 1.0,  1.0)
    glColor4f(clr3[0], clr3[1], clr3[2], clr3[3] * _alpha); glVertex2f( 1.0, -0.0)
    glColor4f(clr4[0], clr4[1], clr4[2], clr4[3] * _alpha); glVertex2f(-0.0, -0.0)
    glEnd()
    glPopMatrix()


colorplane = Colorplane




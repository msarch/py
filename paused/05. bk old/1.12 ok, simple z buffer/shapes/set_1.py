#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * nov 2014 * bw-rev112
adapted from Jonathan Hartley's code
'''

#--- IMPORTS ------------------------------------------------------------------
from utils.cfg import *  # all colors
from utils.math import *
from shapes import Shape

##--- CONSTANTS AND VARIABLES -------------------------------------------------
#--- COMMON SHAPES ------------------------------------------------------------
class Blip(Shape):
    """
    Point, autocad style
    color=color
    """
    def build(self):
        if not hasattr(self,'color'):
            self.color = red
        self.verts = [(-5,0),(5,0),(0,0),(0,5),(0,-5)]
        self.primtype = GL_LINE_STRIP

class Rose(Shape):
    '''
    Oriented Blip : north is marked
    '''
    def build(self):
        if not hasattr(self,'color'):
            self.color = red
        self.verts = [(-5,0),(5,0),(1,0),(1,5),(-1,5),(-1,0),(0,0),(0,-5)]
        self.primtype = GL_LINE_STRIP


class Rect(Shape):
    """
    Rectangle, lower left basepoint is @ origin
    w=width, h=height, color=color
    """

    def build(self):
        if not hasattr(self,'color'):
            self.color = white
        if not hasattr(self,'w'):
            self.w = 100
        if not hasattr(self,'h'):
            self.h = 50

        self.verts = [(0, 0),(self.w, 0),(0, self.h),(self.w, self.h)]
        self.primtype = GL_TRIANGLE_STRIP

        # 2--------3
        # |        |
        # 0--------1


class Kapla(Shape):
    """
    color=color
    """
    def build(self):
        if not hasattr(self,'color'):
            self.color = black
        self.w, self.h = 33,11
        self.verts = [(0,0),(self.w,0),(0,self.h),(self.w,self.h)]
        self.primtype = GL_TRIANGLE_STRIP






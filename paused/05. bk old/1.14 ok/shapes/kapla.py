#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# msarch@free.fr * jan 2015 * bw-rev113

#--- IMPORTS ------------------------------------------------------------------
from pyglet.gl import GL_TRIANGLE_STRIP, GL_LINE_STRIP
from shape import Shape

#--- COMMON SHAPES (RECTANGULAR) ----------------------------------------------
class Kapla(Shape):
    '''
    Rect0 fixed size, color=color
    '''
    def build(self):
        self.w, self.h = 33,11
        self.verts = [(0,0),(self.w,0),(0,self.h),(self.w,self.h)]
        self.primtype = GL_TRIANGLE_STRIP

kapla = Kapla

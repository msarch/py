#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# msarch@free.fr * jan 2015 * bw-rev113

#--- IMPORTS ------------------------------------------------------------------
from shapes.shape import Shape
from pyglet.gl import GL_TRIANGLE_STRIP, GL_LINE_STRIP

#--- COMMON SHAPES (RECTANGULAR) ----------------------------------------------
class Rectangle_0(Shape):
    '''
    Rectangle, Origin @ lower left corner, w=width, h=height, color=color
    2--------3
    |        |
    0--------1
    '''

    def build(self):
        self.primtype = GL_TRIANGLE_STRIP
        if not hasattr(self,'w'):
            self.w = 100
        if not hasattr(self,'h'):
            self.h = 50
        self.verts = [(0, 0),(self.w, 0),(0, self.h),(self.w, self.h)]

rectangle_0 = Rectangle_0

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# msarch@free.fr * jan 2015 * bw-rev113

#--- IMPORTS ------------------------------------------------------------------
from shapes.shape import Shape
from pyglet.gl import GL_TRIANGLE_STRIP, GL_LINE_STRIP

#--- COMMON SHAPES (RECTANGULAR) ----------------------------------------------

class Rectangle(Shape):
    '''
    Centered Rectangle, Origin @ centroid w=width, h=height, color=color
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
        self.verts = [(-self.w/2, -self.h/2),(self.w/2, -self.h/2),\
                (-self.w/2, self.h/2),(self.w/2, self.h/2)]


rectangle = Rectangle
dummy = Rectangle(w=0,h=0)

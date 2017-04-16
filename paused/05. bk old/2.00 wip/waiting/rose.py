#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * jan 2015 * bw-rev113
adapted from Jonathan Hartley's code
'''

#--- IMPORTS ------------------------------------------------------------------
from pyglet.gl import GL_TRIANGLE_STRIP, GL_LINE_STRIP
from engine.shape import Shape


class Rose(Shape):
    '''
    North Oriented Blip : north is a thick line
    '''
    def build(self):
        self.verts = [(-5,0),(5,0),(1,0),(1,5),(-1,5),(-1,0),(0,0),(0,-5)]
        self.primtype = GL_LINE_STRIP

rose = Rose

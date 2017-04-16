#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev107
'''

#--- IMPORTS ------------------------------------------------------------------
from itertools import chain
from collections import OrderedDict

from pyglet.gl import GL_TRIANGLE_STRIP, GL_LINE_STRIP, \
        glPushMatrix, glTranslatef,glRotatef, glPopMatrix
from pyglet.graphics import Batch

from utils.cfg import *


##--- CONSTANTS AND VARIABLES -------------------------------------------------

lmnts = OrderedDict()
##---GENERAL GRAPHIC SHAPE CLASS-------------------------------------------
class Shape(object):
    """
    Stores a list of vertices, a single color, and a primitive type
    Intended to be rendered as a single OpenGL primitive
    """
    def __init__(self, name, **kwargs):
        global lmnts
        if name in lmnts:
            raise ValueError('duplicate shape name', name)
            exit(1)
        elif name == '':
            raise ValueError('no shape name', name)
        else:
            self.name=name
        lmnts[self.name] = self
        print ":: new shape :", self.name
        for i in kwargs:
            setattr(self,i,kwargs[i])
        self.build()
        self.flat_verts = None
        self.batch = None

    def offseted(self, dx, dy):
        newverts = [(v[0] + dx, v[1] + dy) for v in self.verts]
        self.verts=newverts

    def centered(self):
        pass

    def transformed(self,M):
        """ applies matrix M transformation to all self vertexes
        """
        newverts = [ (M[0]*v[0]+M[1]*v[1]+M[2],
                M[3]*v[0]+M[4]*v[1]+M[5]) for v in self.verts]
        return Shape(newverts, self.color, primtype=self.primtype)              #TODO replace shape verts only

    def get_aabb(self):
        _allx=[]
        _ally=[]
        for v in self.verts:
            _allx.append(v[0])
            _ally.append(v[1])
        lox=min(_allx)
        loy=min(_ally)
        hix=max(_allx)
        hiy=max(_ally)
        return (AABB(lox,loy,hix,hiy))

    def get_flat_verts(self):
        if self.flat_verts is None:
            self.flat_verts = \
                list(self.verts[0]) + \
                [x for x in chain(*self.verts)] + \
                list(self.verts[-1])
        return self.flat_verts

    def get_batch(self):
        if self.batch is None:
            self.batch = Batch()
            flatverts = self.get_flat_verts()
            numverts = len(flatverts) / 2
            self.batch.add(
                numverts,
                self.primtype,
                None,
                ('v2f/static', flatverts),
                ('c4B/static', self.color * numverts)
                )
        return self.batch

    def paint(self, peg):
        batch = self.get_batch()
        glPushMatrix()
        glTranslatef(peg.x, peg.y, 0)
        glRotatef(peg.angle, 0, 0, 1)
        batch.draw()
        glPopMatrix()

#--- MULTI SHAPES HOLDER ------------------------------------------------------
# see spreading pyglets wings example
#class Shapes():
#    pass
#   TODO
#   def __add__(self, other):
#    '''Add the shapes from a given shape'''


#--- COMMON SHAPES ------------------------------------------------------------
class Blip(Shape):
    """
    Point, autocad style,
    color=color
    """
    def build(self):
        if not hasattr(self,'color'):
            self.color = red
        self.verts = [(-5,0),(5,0),(0,0),(0,5),(0,-5)]
        self.primtype = GL_LINE_STRIP



class Rect(Shape):
    """
    Rectangle, lower left basepoint is @ origin
    w=width, h=height, color=color
    """

    def build(self):
        if not hasattr(self,'color'):
            self.color = black
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






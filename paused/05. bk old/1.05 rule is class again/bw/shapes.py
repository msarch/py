#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev105
'''

#--- IMPORTS ------------------------------------------------------------------
from itertools import chain
from collections import namedtuple

from pyglet.gl import GL_TRIANGLE_STRIP, GL_LINE_STRIP, \
        glPushMatrix, glTranslatef,glRotatef, glPopMatrix
from pyglet.graphics import Batch

from colors import *


##--- CONSTANTS AND VARIABLES -------------------------------------------------
Point  = namedtuple('Point', 'x y')
Rect   = namedtuple('Rect', 'lox loy hix hiy')
AABB   = namedtuple('AABB', Rect._fields)
Speed  = namedtuple('Speed','vx vy av')
Speed1 = namedtuple('Speed1', 'speed heading')
Speed2 = namedtuple('Speed2', 'x y angle speed')
Peg    = namedtuple('Peg','x y angle')
Peg2   = namedtuple('Peg2', 'x y angle speed head_to') # or use Peg3 ??
Peg3   = namedtuple('Peg3', 'x y angle speed path') # target
Set    = namedtuple('set', 'rulename rule_args subject')

ORIGIN = Point(0.0, 0.0)
IDLE   = Speed(0.0, 0.0, 0.0)
DOCKED = Peg(0.0, 0.0, 0.0)
o = ORIGIN
id = IDLE
dk = DOCKED

setup = []


##---GENERAL GRAPHIC shape CLASS-------------------------------------------
class Gl_Prim(object):
    """
    Stores a list of vertices, a single color, and a primitive type
    Intended to be rendered as a single OpenGL primitive
    """
    def __init__(self, verts, color, primtype=GL_TRIANGLE_STRIP):
        global setup
        self.verts = verts
        self.color = color
        self.primtype = primtype
        self.vertex_list = None
        self.flat_verts = None
        self.batch = None
        self.peg = dk
        self.aabb = self.get_aabb()
        setup.append(self)

    def offset(self, vx, vy):
        newverts = [(v[0] + vx, v[1] + vy) for v in self.verts]
        return Gl_Prim(newverts, self.color, primtype=self.primtype)

    def transform(self,M):
        """ applies matrix M transformation to all self vertexes
        """
        newverts = [ (M[0]*v[0]+M[1]*v[1]+M[2],
                M[3]*v[0]+M[4]*v[1]+M[5]) for v in self.verts]
        return Gl_Prim(newverts, self.color, primtype=self.primtype)

    def peg_to(self, p):
        self.peg = p

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
        glPushMatrix()
        glTranslatef(peg.x, peg.y, 0)
        glRotatef(peg.angle, 0, 0, 1)
        batch = self.get_batch()
        batch.draw()
        glPopMatrix()

class Rect(Gl_Prim):
    """ width, height, color (lower left basepoint is @ origin)
    """
    def __init__(self, w, h, color = black):
        verts=[(0,0),(w,0),(0,h),(w,h)]
        # 2--------3
        # |        |
        # 0--------1
        Gl_Prim.__init__ (self,verts,color, GL_TRIANGLE_STRIP)

class Kapla(Gl_Prim):
    """ color (lower left basepoint is @ origin)
    """
    def __init__(self, color = black):
        verts=[(0,0),(33,0),(0,11),(33,11)]
        Gl_Prim.__init__ (self,verts,color, GL_TRIANGLE_STRIP)

class Blip(Gl_Prim):
    def __init__(self,color=red):
        verts=[(-5,0),(5,0),(0,0),(0,5),(0,-5)]
        Gl_Prim.__init__ (self,verts,color, GL_LINE_STRIP)


#---MULTI shapeS HOLDER----------------------------------------------------

#class Layer():
#   TODO
#   def __add__(self, other):
#    '''Add the shapes from a given shape'''





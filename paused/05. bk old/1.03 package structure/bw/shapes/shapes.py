#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * july 2014 * bw-rev103
'''

#--- IMPORTS ------------------------------------------------------------------
from itertools import chain
from pyglet.graphics import vertex_list
from pyglet.gl import GL_TRIANGLE_STRIP, glPushMatrix, glTranslatef,\
    glRotatef, glPopMatrix
from pyglet.graphics import Batch
from colors import Color
from .. debug import db_print


##--- CONSTANTS AND VARIABLES -------------------------------------------------

##---GENERAL GRAPHIC PRIMITIVE CLASS-------------------------------------------
class Primitive(object):
    """
    Stores a list of vertices, a single color, and a primitive type
    Intended to be rendered as a single OpenGL primitive
    """
    def __init__(self, verts=None, color=Color.white, primtype=GL_TRIANGLE_STRIP):
        self.verts = verts
        self.color = color
        self.primtype = primtype
        self.vertex_list = None
        self.flat_verts = None

    def transform(self,M):
        """ applies matrix M transformation to all self vertexes
        """
        for index, v in enumerate(self.verts):
            self.verts[index] = [M[0]*v[0]+M[1]*v[1]+M[2],\
                                 M[3]*v[0]+M[4]*v[1]+M[5]]

    def offset(self, dx, dy):
        newverts = [(v[0] + dx, v[1] + dy) for v in self.verts]
        return Primitive(newverts, self.color, primtype=self.primtype)

    def rotate(self, alpha):
        print 'rotate not implemented'
        return(self)

    def get_flat_verts(self):
        if self.flat_verts is None:
            self.flat_verts = \
                list(self.verts[0]) + \
                [x for x in chain(*self.verts)] + \
                list(self.verts[-1])
        return self.flat_verts

    def get_vertexlist(self):
        if self.vertex_list is None:
            flatverts = self.get_flat_verts()
            numverts = len(flatverts) / 2
            self.vertex_list = vertex_list(
                numverts,
                ('v2f/static', flatverts),
                ('c3B/static', self.color * numverts))
        return self.vertex_list


# TODO
    #@property
    #def type(self):
        #return (self.__class__)

    #@property
    #def M(self):
        #return (self._M)

    #@M.setter
    #def M(self,matrix):
        #self._M = matrix

    #@property
    #def color(self):
        #return (self._color)

    #@color.setter
    #def color(self,c):
        #self._color = c

    #def __repr__(self):
       #return "Rec\tw,h:(%.1dx%.1d), @(%.1d,%1d), \t\tM%3s" \
       #% (self.width(), self.height(), self.v[0][0], self.v[0][1], self.M)

    #def copy(self):
        #rect=Rect(self.width,self.height,self.v[0][0],self.v[0][1],self.color,self.M)
        #return rect


#---MULTI PRIMITIVES HOLDER----------------------------------------------------
class Shape(object):
    '''
    A list of primitives
    '''
    def __init__(self, items=None):
        self.primitives = []
        self.batch = None
        self.aabb = (0,0,0,0)
        if items:
            self.add_items(items)
            self.get_aabb()

    def add_items(self, items):
        "Add a list of primitives and shapes"
        for item in items:
            if isinstance(item, Shape):
                self.add_shape(item)
            else:
                self.primitives.append(item)

    def add_shape(self, other):
        "Add the primitives from a given shape"
        for prim in other.primitives:
            self.primitives.append(prim)

    def get_batch(self):
        if self.batch is None:
            self.batch = Batch()
            for prim in self.primitives:
                flatverts = prim.get_flat_verts()
                numverts = len(flatverts) / 2
                self.batch.add(
                    numverts,
                    prim.primtype,
                    None,
                    ('v2f/static', flatverts),
                    ('c3B/static', prim.color * numverts)
                )
                print (
                    numverts,
                    prim.primtype,
                    None,
                    ('v2f/static', flatverts),
                    ('c3B/static', prim.color * numverts)
                )

        return self.batch

    def transform(self,M):
        """ applies matrix M to all self primitives
        """
        for prim in self.primitives:
            prim.transform(M)

    def get_aabb(self):
        _allx=[]
        _ally=[]
        for prim in self.primitives:
            for v in prim.verts:
                _allx.append(v[0])
                _ally.append(v[1])
        self.aabb = (min(_allx), min(_ally), max(_allx), max(_ally))

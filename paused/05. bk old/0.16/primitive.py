!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: primitive :: rev 16 :: 02.2014 :: msarch@free.fr

from itertools import chain
from pyglet.graphics import vertex_list
from pyglet.gl import GL_TRIANGLE_STRIP


##--- CONSTANTS AND VARIABLES -------------------------------------------------


##--- CLASSES -----------------------------------------------------------------
class Color(object):
    orange = (255, 127, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    red = (200, 0, 0)
    blue = (127, 127, 255)
    pink = (255, 187, 187)
    very_light_grey=(0.95, 0.95, 0.95, 0)

class Primitive(object):
    """
    Stores a list of vertices, a single color, and a primitive type
    Intended to be rendered as a single OpenGL primitive
    """
    def __init__(self, verts, color, primtype=GL_TRIANGLE_STRIP):
        self.verts = verts
        self.color = color
        self.primtype = primtype
        self.vertex_list = None
        self.flat_verts = None

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


#--- COMMON PRIMITIVES ---------------------------------------------------------------

class Rect(Primitive):
    """ (basepoint x,basepoint y), width, height,color
    v2                             v3
      +---------------------------+
      |                           |
      |                           |
      +---------------------------+
    vO                             v1

    glBegin(GL_TRIANGLE_STRIP);
    glVertex3fv(v0);
    glVertex3fv(v1);
    glVertex3fv(v2);
    glVertex3fv(v3);
    glEnd();
    """
    def __init__(self,x,y,w,h,color):
        verts=[(x,y),(x+w,y),(x,y+h),(x+w,y+h)]
        Primitive.__init__ (self,verts,color, GL_TRIANGLE_STRIP)

def Blip(x,y):
    print 'blip not implemented'
    pass

def Point(x,y):
    print 'point not implemented'
    pass



#!/usr/bin/python
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus :: rev 13-d3 :: 10.2013 :: msarch@free.fr

##  TO DO LIST ----------------------------------------------------------------
# TODO : COLOR STROKE & FILL
# use named colors module -->ie styles module?
# kwd : program style

##--- IMPORTS -----------------------------------------------------------------
import pyglet
from pyglet.graphics import Batch,draw
from math import sin,cos


##--- CONSTANTS AND VARIABLES -------------------------------------------------

##--- CLASSES -----------------------------------------------------------------
from pyglet.gl import GL_TRIANGLE_STRIP

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

    def offset(self, dx, dy):
        newverts = []
        for i in range(0, len(self.verts), 2):
            newverts += [self.verts[i]+dx,self.verts[i+1]+dy]
        return Primitive(newverts, self.color, primtype=self.primtype)

    def rotate(self, angle):
        newverts = []
        angle = -angle # no idea
        for i in range(0, len(self.verts), 2):
            x, y = self.verts[i], self.verts[i+1]
            newverts += [
                x * cos(angle) - y * sin(angle),
                y * cos(angle) + x * sin(angle) ]
        return Primitive(newverts, self.color, primtype=self.primtype)

class Body(object):
    "A list of primitives. Creates a single batch to draw these primitives."
    def __init__(self, items=None):
        self.primitives = []
        if items:
            self.add_items(items)
        self.batch = None

    def add_items(self, items):
        "'items' may contain primitives and/or bodys"
        for item in items:
            if isinstance(item, Body):
                for prim in item.primitives:
                    self.primitives.append(prim)
            else:
                self.primitives.append(item)

    def batch_draw(self):
        if self.batch is None:
            self.batch = Batch()
            for primitive in self.primitives:
                batchVerts = \
                    [primitive.verts[0], primitive.verts[1]] + \
                    primitive.verts + \
                    [primitive.verts[-2], primitive.verts[-1]]
                numverts = len(batchVerts) / 2
                self.batch.add(
                        numverts,
                    primitive.primtype,
                    None, # draw order group to be implemented later
                    ('v2f/static', batchVerts),
                    ('c3B/static', primitive.color * numverts),
                    )
        self.batch.draw()




#--- FUNCTIONS  ---------------------------------------------------------------
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
        verts=(x,y,x+w,y,x,y+h,x+w,y+h)
        Primitive.__init__ (self,verts,color, GL_TRIANGLE_STRIP)

def Blip(x,y):
    print 'blip not implemented'
    pass

def Point(x,y):
    print 'point not implemented'
    pass




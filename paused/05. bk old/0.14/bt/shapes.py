#!/usr/bin/python
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus :: rev 13-e :: 12.2013 :: msarch@free.fr


##--- IMPORTS -----------------------------------------------------------------
import pyglet
from pyglet.graphics import Batch,draw
from math import sin,cos
from pyglet.gl import GL_TRIANGLE_STRIP


##--- CONSTANTS AND VARIABLES -------------------------------------------------


##--- BODY SUPER CLASS --------------------------------------------------------
class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


##--- BODY CLASS --------------------------------------------------------------

class Body(object):
    "A list of shapes. Creates a single batch to draw these shapes."
    __metaclass__ = IterRegistry
    _registry = []
    def __init__(self,items=None,anchor=[0,0],angle=0,drawable=True):
        self.shapes = []
        self._registry.append(self)
        self.body=body
        self.anchor=anchor
        self.angle=angle
        self.drawable=drawable
        if items:
            self.add_items(items)
        self.batch = None

    def add_items(self, items):
        "'items' may contain shapes and/or bodies"
        for item in items:
            if isinstance(item, Body):
                for shp in item.shapes:
                    self.shapes.append(shp)
            else:
                self.shapes.append(item)

    def batch_draw(self):
        if self.batch is None:
            self.batch = Batch()
            for shape in self.shapes:
                batchVerts = \
                    [shape.verts[0], shape.verts[1]] + \
                    shape.verts + \
                    [shape.verts[-2], shape.verts[-1]]
                numverts = len(batchVerts) / 2
                self.batch.add(
                        numverts,
                    shape.primtype,
                    None, # draw order group to be implemented later
                    ('v2f/static', batchVerts),
                    ('c3B/static', shape.color * numverts),
                    )
        self.batch.draw()



    def paint_all():
        for z in Zulu:
            glPushMatrix()
            glTranslatef(z.anchor[0],z.anchor[1],0)   # Move bac
            glRotatef(z.angle, 0, 0, 1)
            z.body.batch_draw()
            glPopMatrix()

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


class Shape(object):
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
        return Shape(newverts, self.color, primtype=self.primtype)

    def rotate(self, angle):
        newverts = []
        angle = -angle # no idea
        for i in range(0, len(self.verts), 2):
            x, y = self.verts[i], self.verts[i+1]
            newverts += [
                x * cos(angle) - y * sin(angle),
                y * cos(angle) + x * sin(angle) ]
        return Shape(newverts, self.color, primtype=self.primtype)





#--- FUNCTIONS  ---------------------------------------------------------------
#--- COMMON shapes --------------------------------------------------------

class Rect(Shape):
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
        Shape.__init__ (self,verts,color, GL_TRIANGLE_STRIP)

def Blip(x,y):
    print 'blip not implemented'
    pass

def Point(x,y):
    print 'point not implemented'
    pass




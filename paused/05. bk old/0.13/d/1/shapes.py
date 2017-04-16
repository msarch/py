#!/usr/bin/python
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus :: rev 13-d :: 10.2013 :: msarch@free.fr

##--- IMPORTS -----------------------------------------------------------------

from pyglet.gl import *
import pyglet

##--- CONSTANTS AND VARIABLES -------------------------------------------------

##--- CLASSES -----------------------------------------------------------------

class Shape(object):

    def draw(self,position):
        """ draw to screen,
        should be defined by each subclass
        """
        pass

#--- POINT -------------------------------------------------------------------------------------------

class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def _get_xy(self):
        return (self.x, self.y)
    def _set_xy(self, (x,y)):
        self.x = x
        self.y = y

    xy = property(_get_xy, _set_xy)

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return "Point(x=%.1f, y=%.1f)" % (self.x, self.y)

    def __eq__(self, pt):
        if not isinstance(pt, Point): return False
        return self.x == pt.x \
           and self.y == pt.y

    def __ne__(self, pt):
        return not self.__eq__(pt)

class Rect(Shape):
    """ rectangle is a shape attribute defined by :
            initial x,y axis, width, height as args
            initial x,y speed,color are kwargs
            AABB
    """
    def __init__(self,width=300, height=100):
        # self vertex list:
        #                             centroid,     [0]
        #                             bottom left,  [1]
        #                             bottom right, [2]
        #                             top right,    [3]
        #                             top left      [4]
        self.width=width
        self.height=height
        self.vtx=[[-self.width*0.5,-self.height*0.5],\
                        [self.width*0.5,-self.height*0.5],\
                        [self.width*0.5,self.height*0.5],\
                        [-self.width*0.5,self.height*0.5],]


    def draw(self, position,color):
        """ Draws the rectangle with the bottom left corner at x, y.
        The current stroke, strokewidth and fill color are applied.
        """
        glTranslatef(position[0],position[1],position[2])   # Move Origin
        pyglet.gl.glColor3f(color[0],color[1],color[2])
        glBegin(GL_QUADS)
        glVertex3f(self.vtx[0][0], self.vtx[0][1], 0.0)  # bottom left
        glVertex3f(self.vtx[1][0], self.vtx[1][1], 0.0)  # bottom right
        glVertex3f(self.vtx[2][0], self.vtx[2][1], 0.0)  # top right
        glVertex3f(self.vtx[3][0], self.vtx[3][1], 0.0)  # top left
        glEnd()

        glTranslatef(-position[0],-position[1],-position[2])   # Move back


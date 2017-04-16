#!/usr/bin/python
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus :: rev 13-b :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------



##--- IMPORTS -----------------------------------------------------------------

from pyglet.gl import *

##--- CONSTANTS AND VARIABLES -------------------------------------------------

##--- CLASSES -----------------------------------------------------------------

class Shape(object):

    def draw(self,centroid,color):
        """ draw to screen,
        should be defined by each subclass
        """
        pass

class Phantom(Shape):
    """ Dummy """
    def __init__(self):
        pass

    def draw(self,centroid,color):
        pass

class Rect(Shape):
    """ rectangle is a shape defined by half width, half height
    centroid is the anchor point
    """
    def __init__(self,w=150, h=150):
        # self vertex list, counterclockwise from bottom left
        #                             centroid,     [0]
        #                             bottom left,  [1]
        #                             bottom right, [2]
        #                             top right,    [3]
        #                             top left      [4]
        self.h=h
        self.w=w
        self.vtx=[[-self.w,-self.h],[self.w,-self.h],[self.w,self.h],[-self.w,self.h],]

    def draw(self, centroid=[0,0,0],color=[123,222,32]):
        """ Draws the rectangle with the bottom left corner at x, y.
        The current stroke, strokewidth and fill color are applied.
        """
        # Set color
        pyglet.gl.glColor3f(color[0],color[1],color[2])
        # Mv glOrigin to centroid
        glTranslatef(centroid[0],centroid[1],centroid[2])

        glBegin(GL_QUADS)
        glVertex3f(self.vtx[0][0], self.vtx[0][1], 0.0)  # bottom left
        glVertex3f(self.vtx[1][0], self.vtx[1][1], 0.0)  # bottom right
        glVertex3f(self.vtx[2][0], self.vtx[2][1], 0.0)  # top right
        glVertex3f(self.vtx[3][0], self.vtx[3][1], 0.0)  # top left
        glEnd()

        glTranslatef(-centroid[0],-centroid[1],0.0)   # Move glOrigin back



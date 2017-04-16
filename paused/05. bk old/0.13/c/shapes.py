#!/usr/bin/python
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus :: rev 13-c :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------



##--- IMPORTS -----------------------------------------------------------------

from pyglet.gl import *

##--- CONSTANTS AND VARIABLES -------------------------------------------------

##--- CLASSES -----------------------------------------------------------------

class Shape(object):

    def draw(self,position):
        """ draw to screen,
        should be defined by each subclass
        """
        pass


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

        pyglet.gl.glColor3f(123,222,32)
        glTranslatef(position[0],position[1],0.0)   # Move Origin to screen center

        glBegin(GL_QUADS)
        glVertex3f(self.vtx[0][0], self.vtx[0][1], 0.0)  # bottom left
        glVertex3f(self.vtx[1][0], self.vtx[1][1], 0.0)  # bottom right
        glVertex3f(self.vtx[2][0], self.vtx[2][1], 0.0)  # top right
        glVertex3f(self.vtx[3][0], self.vtx[3][1], 0.0)  # top left
        glEnd()

        glTranslatef(-position[0],-position[1],0.0)   # Move Origin to screen center



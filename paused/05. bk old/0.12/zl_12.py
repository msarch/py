#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 07.2013
# what : pyglet animation

# zl_12

##--- CONSTANTS AND VARIABLES -------------------------------------------------
pt=5        # point display size
pool=[]     # list of all recs in the scene

##--- IMPORTS -----------------------------------------------------------------
from pyglet.gl import *
from matrix_operations import *
from zululand import Zululand, Zulu

##--- BOUNCING RECTANGLE (ortho) ----------------------------------------------
class B_Rec(Zulu):
    """ rectangle is a Zulu defined by :
            initial x,y axis, width, height as args
            initial x,y speed,color are kwargs
            XYBB
    """
    def __init__(self, x=0, y=0, width=300, height=100, \
                 vx=3, vy=0, color=(100,0,0)):
        # self vertex list:
        #                             centroid,     [0]
        #                             bottom left,  [1]
        #                             bottom right, [2]
        #                             top right,    [3]
        #                             top left      [4]
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vx=vx
        self.vy=vy

        self.vtx=[[self.x,self.y],[self.x-self.width*0.5,self.y-self.height*0.5],\
                        [self.x+self.width*0.5,self.y-self.height*0.5],\
                        [self.x+self.width*0.5,self.y+self.height*0.5],\
                        [self.x-self.width*0.5,self.y+self.height*0.5],]
        self.color = color

    @property
    def type(self):
        return (self.__class__)

    @property
    def color(self):
        return (self._color)

    @color.setter
    def color(self,c):
        self._color = c


    def matrix_apply(self,M):
        """ applies matrix M transformation
        to all transformable vertex, incl the centroid.
        """
        for index, vtx in enumerate(self.vtx):
            self.vtx[index] = [self.M[0]*vtx[0]+self.M[1]*vtx[1]+self.M[2],\
                             self.M[3]*vtx[0]+self.M[4]*vtx[1]+self.M[5]]


    def __repr__(self):
       return "Rec\tw,h:(%.1dx%.1d), @(%.1d,%1d), \t\tM%3s" \
       % (self.width(), self.height(), self.vtx[0][0], self.vtx[0][1], self.M)

    def copy(self):
        new_rect=Rect(self.width(),self.height(),self.vtx[0][0],self.vtx[0][1],self.color,self.M)
        return new_rect

    def width(self):
        return(distance(self.vtx[1][0], self.vtx[1][1], self.vtx[2][0], self.vtx[2][1]))

    def height(self):
        return(distance(self.vtx[1][0], self.vtx[1][1], self.vtx[4][0], self.vtx[4][1]))

    def update(self, dt):
        # move the ball according to simple physics
        self.x += self.vx
        self.y += self.vy
        print self.y
        # reflect the ball if is in contact with the top of the playing area
        if self.y > 500-4:
            self.y = 500-4
            self.vy = -self.vy
        # and the same for the bottom
        elif self.y < 4:
            self.y = 4
            self.vy = -self.vy

        # reflect the ball right
        if self.x > 800-8:
            self.x = 800-8
            self.vx = -self.vx
        # change the velocity based on the distance to the center of the paddle

        #  left
        elif self.x < 8:
            self.x = 8
            self.vx = -self.vx


        self.vtx=[[self.x,self.y],[self.x-self.width*0.5,self.y-self.height*0.5],\
                        [self.x+self.width*0.5,self.y-self.height*0.5],\
                        [self.x+self.width*0.5,self.y+self.height*0.5],\
                        [self.x-self.width*0.5,self.y+self.height*0.5],]

    def draw(self, **kwargs):
        """ Draws the rectangle with the bottom left corner at x, y.
        The current stroke, strokewidth and fill color are applied.
        """
        pyglet.gl.glColor3f(self.color[0],self.color[1],self.color[2])
        glBegin(GL_QUADS)
        glVertex3f(self.vtx[1][0], self.vtx[1][1], 0.0)  # bottom left
        glVertex3f(self.vtx[2][0], self.vtx[2][1], 0.0)  # bottom right
        glVertex3f(self.vtx[3][0], self.vtx[3][1], 0.0)  # top right
        glVertex3f(self.vtx[4][0], self.vtx[4][1], 0.0)  # top left
        glEnd()



##  MAIN ----------------------------------------------------------------------
def main():
    ZL12=Zululand()
# zulus
    z1=B_Rec(5,5,200,300)
    ZL12.append(z1)

    z2=B_Rec(100,200,10,2)
    ZL12.append(z2)
# run the application
    ZL12.run()

##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()

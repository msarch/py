#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: rules :: rev 13-d :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from zululand import Rule

#--- RULES --------------------------------------------------------------------

class Listen(Rule):
    """ parse available data.
    """
    def update(self,dt):
        """ do one step for every member this rule has.
        """
        for z in self.group:
            pass

class Publish(Rule):
    """ broadcast data.
    """
    def update(self,dt):
        """ do one step for every member this rule has.
        """
        for z in self.group:
            pass

class matrix_mult(Rule):
    """ applies matrix M transformation
    to all transformable vertex, incl the centroid.
    """
    def update(self,dt):
        """ do one step for every member this rule has.
        """
        M=self.M
        for z in self.group:
            for index, vtx in enumerate(z.vtx):
                z.vtx[index] = [M[0]*vtx[0]+M[1]*vtx[1]+M[2],\
                        M[3]*vtx[0]+M[4]*vtx[1]+M[5]]

class Slide(Rule):
    def __init__(self,vx=0,vy=0):
        super(Slide, self).__init__()
        self.vx=vx
        self.vy=vy

    def apply(self,z,dt):
        """ what happens to every member this rule has.
        """
        z.position[0]+= self.vx*dt
        z.position[1]+= self.vy*dt

class Bounce(Rule):
    def apply(z, dt):
        # reflect the ball if is in contact with the top of the playing area
        if z.y > 500-4:
            z.y = 500-4
            z.vy = -z.vy
        # and the same for the bottom
        elif z.y < 4:
            z.y = 4
            z.vy = -z.vy

        # reflect the ball right
        if z.x > 800-8:
            z.x = 800-8
            z.vx = -z.vx
        # change the velocity based on the distance to the center of the paddle

        #  left
        elif z.x < 8:
            z.x = 8
            z.vx = -z.vx


        z.vtx=[[z.x,z.y],[z.x-z.width*0.5,z.y-z.height*0.5],\
                        [z.x+z.width*0.5,z.y-z.height*0.5],\
                        [z.x+z.width*0.5,z.y+z.height*0.5],\
                        [z.x-z.width*0.5,z.y+z.height*0.5],]

def camera_apply(target):
        x=camerax
        y=cameray
        return target[0] + x, target[1] + y

def sort():
    """ list all available rules, then sort the list in priority order
    """
    pass

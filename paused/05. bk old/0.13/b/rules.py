#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: rules :: rev 13-b :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
#--- RULES --------------------------------------------------------------------

class Rule(object):

    book=[]
    def __init__(self):
        self.book.append(self)
        self.group=[]

    def apply_to(self,*args):
        """ adds one or more zulus to the rule pool
        """
        for z in args:
            self.group.append(z)

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

class MatrixOp(Rule):
    """ applies matrix M transformation
    to all transformable vertex, incl the centroid.
    """
    def __init__(self,M):
        super(MatrixOp, self).__init__()
        self.M=M

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

    def update(self,dt):
        """ do one step for every member this rule has.
        """
        for z in self.group:
            z.centroid[0]+= self.vx*dt
            z.centroid[1]+= self.vy*dt

class Bounce(Rule):

    def __init__(self,boundaries):
        super(Bounce, self).__init__()


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
 :       # change the velocity based on the distance to the center of the paddle

        #  left
        elif z.x < 8:
            z.x = 8
            z.vx = -z.vx


        z.vtx=[[z.x,z.y],[z.x-z.width*0.5,z.y-z.height*0.5],\
                        [z.x+z.width*0.5,z.y-z.height*0.5],\
                        [z.x+z.width*0.5,z.y+z.height*0.5],\
                        [z.x-z.width*0.5,z.y+z.height*0.5],]



def sort():
    """ list all available rules, then sort the list in priority order
    """
    pass

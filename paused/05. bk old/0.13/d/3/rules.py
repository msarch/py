#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: rules :: rev 13-d3 :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------

#--- RULE ---------------------------------------------------------------------

class Ruleset(object):
            ###############################
            #  / _(_)_  ___ __ ___   ___  #
            # | |_| \ \/ / '_ ` _ \ / _ \ #
            # |  _| |>  <| | | | | |  __/ #
            # |_| |_/_/\_\_| |_| |_|\___| #
            ###############################
    """ ruleset is a dictionary, holding :
    keys :  string : rule name
    values : list of zulus to which the rule applies
    """
    def __init__(self):
        self.dict_={}


    def sort(self):
        """ sort the ruleset in priority order
        """
        pass


    def list(self):
        """ list of rules and related zulus
        """
        pass

    def sort(self):
        pass

    def add(self,rule,*args):
        """ adds one or more zulus to the rule pool
        """
        zlist=list(args)
        self.dict_[rule] = zlist
        print self.dict_
        #self._dict.

    def remove(self,rule,*args):
        """ adds one or more zulus to the rule pool
        """
        pass

    def update(self,dt,chrono):
        for rule,zlist in self.dict_.iteritems():
            for z in zlist:
                rule.apply(z,dt,chrono)

class Rule(object):

    def apply(self, z,dt, chrono):
        print self, 'apply not implemented'

#--- RULES --------------------------------------------------------------------
class Listen(Rule):
    """ parse available data.
    """
    def apply(self,z,dt,chrono):
        """ do one step for every member this rule has.
        """
        pass

class Publish(Rule):
    """ broadcast data.
    """
    def apply(self,z,dt,chrono):
        """ do one step for every member this rule has.
        """
        for z in self.group:
            pass

class matrix_mult(Rule):
    """ applies matrix M transformation
    to all transformable vertex, incl the centroid.
    """
    def __init__(self,M):
        super(matrix_mult, self).__init__()
        self.m=M # matrix

    def apply(self,z,dt,chrono):
        """ do one step for every member this rule has.
        """
        M=self.m
        for z in self.group:
            for index, vtx in enumerate(z.vtx):
                z.vtx[index] = [M[0]*vtx[0]+M[1]*vtx[1]+M[2],\
                        M[3]*vtx[0]+M[4]*vtx[1]+M[5]]

class Slide(Rule):
    def __init__(self,speed):
        #super(Slide, self).__init__()
        self.vx,self.vy=speed # two values tuple

    def apply(self,z,dt,chrono):
        """ what happens to every member this rule has.
        """
        z.anchor[0]+= self.vx*dt
        z.anchor[1]+= self.vy*dt

class FadeOut(Rule):
    # TODO
    pass

class Bounce(Rule):
    def apply(self,z,dt,chrono):
        # reflect the ball if is in contact with the top of the playing area
        if z.y > 500-4:
            z.y = 500-4
            z.vy = -z.vy
        # and the same for the bochronoom
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

class camera_shift(Rule):

    def __init__(self,camera_x=0,camera_y=0):
        super(Slide, self).__init__()
        self.dx=camera_x
        self.dy=camera_y


    def apply(self,z,dt,chrono):
        """ what happens to every member this rule has.
        """

        z.anchor[0]+= -self.dx
        z.anchor[1]+= -self.dy

#--- FUNCTIONS  ---------------------------------------------------------------


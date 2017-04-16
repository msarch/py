#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: rules :: rev 13-d2 :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------

#--- RULE ---------------------------------------------------------------------


class Rule(object):

    ruleset=[]
    def __init__(self):
        Rule.ruleset.append(self)
        self.zulus=[]

    def add(self,*args):
        """ adds one or more zulus to the rule pool
        """
        for z in args:
            self.zulus.append(z)

    def remove(self,*args):
        """ adds one or more zulus to the rule pool
        """
        for z in args:
            self.zulus.remove(z)

    def list(self):
        """ list of zulus or zulus args? concerned by the rule
        """
        pass

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
    def __init__(self,speed):
        super(Slide, self).__init__()
        self.vx,self.vy=speed # two values tuple

    def apply(self,z,dt):
        """ what happens to every member this rule has.
        """
        z.x+= self.vx*dt
        z.y+= self.vy*dt

class FadeOut(Rule):
    # TODO
    pass

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

class camera_shift(Rule):

    def __init__(self,camera_x=0,camera_y=0):
        super(Slide, self).__init__()
        self.dx=camera_x
        self.dy=camera_y


    def apply(self,z,dt):
        """ what happens to every member this rule has.
        """
        z.position[0]+= -self.dx
        z.position[1]+= -self.dy

def sort():
    """ list all available rules, then sort the list in priority order
    """
    pass

def tick_all(dt):
    """ apply all rules to all of its own zulus
    """
    [[rule.apply(z,dt) for z in rule.zulus]for rule in Rule.ruleset]


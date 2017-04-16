#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev105
'''

##--- IMPORTS -----------------------------------------------------------------
ruleset =[]
##--- Globals -----------------------------------------------------------------

class Rule(object):
    global ruleset
    def __init__(self,**d):
        for i in d:
            setattr(self,i,d[i])
        ruleset.append(self)

    def tick(self,dt):
        pass

##--- MOVE RULES --------------------------------------------------------------
# TODO : replace with general OpenGL? matrix transform

class Step(Rule):
    def tick(self, dt):  # simple dx and dy displacement
        self.shape.peg = self.shape.peg._replace(
                x = self.shape.peg.x + self.dx * dt,
                y = self.shape.peg.y + self.dy * dt)

class Spin(Rule):
    def tick(self, dt):
        self.shape.peg = self.shape.peg._replace(
                angle = self.shape.peg.angle + self.av * dt)

# TODO : following rules need a vector, point, and derivatives
# i.e. speed vector, angular velocity or matrix
# attached to the shape itself and no more to the rule.
# ex : avoid pb BETWEEN rules : bounce
class Cruise(Rule):  # heads to a direction (angle) forever
    def tick(self, dt):
        pass

class Head_to(Rule):
    def tick(self, dt):  # goes towards the head_to point and beyond
        pass

class Look_at(Rule):
    def tick(self, dt):  # orients itself towards the look_at point
        pass

class Walk_path(Rule):
    def tick(self, dt):  # exits and reenters the Rect the oposite side
        pass

##--- COLLISION RULES ---------------------------------------------------------
class Bounce(Rule):
    def tick(self, dt):
        if (self.shape.peg.x - self.shape.aabb[0] < self.rec.lox
                or self.shape.aabb[0] + self.shape.peg.x > self.rec.hix):
            # if bounce, reverse speed and move once
            self.shape.peg = self.shape.peg._replace(
                x = self.shape.peg.x - self.shape.peg.vx * dt,
                y = self.shape.peg.y + self.shape.peg.vy * dt,
                vx = self.shape.peg.vx * -1.0
                )
            # self.shape.color = choice(kapla_colors)      # change clr
        elif (self.shape.peg.y - self.shape.aabb[1] < self.rec.loy
                or self.shape.aabb[3] + self.shape.peg.y > self.rec.hiy):
            self.shape.peg = self.shape.peg._replace(
                x = self.shape.peg.x + self.shape.peg.vx * dt,
                y = self.shape.peg.y - self.shape.peg.vy * dt,
                vy = self.shape.peg.vy * -1.0
                )
            # TODO dispatch flag shp.bounce =1
        else :
            pass

class Wrap(Rule):
    def tick(self, dt):  # exits and reenters the Rect the oposite side
        pass

##--- META RULES --------------------------------------------------------------
class Lifespan(Rule):
    def tick(self, dt):
        ''' Timetable or scenario class
        - keeps track for every rule of a start and end time for each cell
        - can be dict read from text file
        '''
        pass

def remove(rule, shp):
# if rule,shp in dict, remove...
    pass


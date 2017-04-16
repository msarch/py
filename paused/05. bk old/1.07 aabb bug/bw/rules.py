#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev107
'''

##--- IMPORTS -----------------------------------------------------------------
from collections import OrderedDict
import actors

##--- CONSTANTS AND VARIABLES -------------------------------------------------
ruleset = OrderedDict()

##--- RULE CLASS --------------------------------------------------------------
class Rule(object):

    def __init__(self, name, **kwargs):
        global ruleset
        if name in ruleset:
            raise ValueError('duplicate rule name', name)
            exit(1)
        elif name == '':
            raise ValueError('no rule name', name)
        else:
            self.name=name
        ruleset[self.name] = self
        for i in kwargs:
            setattr(self,i,kwargs[i])
        print ":: new rule :", self.name, self.actors

    def tick(self,dt, actor):  # this is the method that defines the action
        pass

##--- MOVE RULES --------------------------------------------------------------
# TODO : replace with general OpenGL? matrix transform : see euclid.py

class Slide(Rule):

    def tick(self, dt, c):  # simple dx and dy displacement
            c.peg = c.peg._replace(
                x = c.peg.x + c.vel.vx * dt,
                y = c.peg.y + c.vel.vy * dt,
                angle = c.peg.angle)

class Spin(Rule):
    def tick(self, dt, actor):
        self.shape.peg = self.shape.peg._replace(
                angle = self.shape.peg.angle + self.av * dt)

# TODO : following rules need a vector, point, and derivatives
# i.e. speed vector, angular velocity or matrix
# attached to the shape itself and no more to the rule.
# ex : avoid pb BETWEEN rules : bounce
class Cruise(Rule):  # heads to a direction (angle) forever
    def tick(self, dt, actor):
        pass

class Head_to(Rule):
    def tick(self, dt, actor):  # goes towards the head_to point and beyond
        pass

class Look_at(Rule):
    def tick(self, dt, actor):  # orients itself towards the look_at point
        pass

class Walk_path(Rule):
    def tick(self, dt, actor):  # exits and reenters the Rect the oposite side
        pass

##--- COLLISION RULES ---------------------------------------------------------
class Bounce(Rule):
    def tick(self, dt, c):
        if (c.peg.x - c.aabb.lox < self.rect.lox
                or c.aabb.hix + c.peg.x > self.rect.hix):
            # if bounce, reverse speed and move once
            c.peg = c.peg._replace(
                    x = c.peg.x - c.vel.vx * dt,
                    y = c.peg.y + c.vel.vy * dt)
            c.vel = c.vel._replace(vx = c.vel.vx * -1.0)
            print c.aabb, self.rect
            # self.shape.color = choice(kapla_colors)      # change clr
        elif (c.peg.y - c.aabb.loy < self.rect.loy
                or c.aabb.hiy + c.peg.y > self.rect.hiy):
            c.peg = c.peg._replace(
                    x = c.peg.x + c.vel.vx * dt,
                    y = c.peg.y - c.vel.vy * dt)
            c.vel = c.vel._replace(vy = c.vel.vy * -1.0)
            # TODO dispatch flag shp.bounce =1
            print c.aabb, self.rect

        else :
            pass

class Wrap(Rule):
    def tick(self, dt, actor):  # exits and reenters the Rect the oposite side
        pass


##--- META RULES --------------------------------------------------------------
# meta rules are given a rule name as argument
# other rules can have their parameters modified, deleted, reordered

class Lifespan(Rule):
    def tick(self, dt, actor):
        ''' Timetable or scenario class
        - keeps track for every rule of a start and end time for each actor
        - can be dict read from text file
        '''
        pass

#--- FUNCS --------------------------------------------------------------------
def tick(dt):
    for rulename in ruleset:
        for actor in ruleset[rulename].actors:
            ruleset[rulename].tick(dt, actors.cast[actor])

def remove(rule, shp):
# if rule,shp in dict, remove...
    pass
 #--- NOTES --------------------------------------------------------------------
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
'''



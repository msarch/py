#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev109
'''

##--- IMPORTS -----------------------------------------------------------------
from collections import OrderedDict
from itertools import cycle
import pyglet
from actors import cast
from shapes import lmnts
import shapes
from events import publish, subscribe, _events
##--- CONSTANTS AND VARIABLES -------------------------------------------------
oneshot_rules = OrderedDict()
rules = OrderedDict()
conditional_rules = OrderedDict()
##--- RULE CLASS --------------------------------------------------------------
class Rule(object):

    def __init__(self, name, **kwargs):
        global rules, conditional_rules, oneshot_rules

        for i in kwargs:
            setattr(self,i,kwargs[i])

        if name in rules:
            raise ValueError('duplicate rule name', name)
            exit(1)
        elif name == '':
            raise ValueError('no rule name', name)
        else:
            self.name=name
        if hasattr(self, 'period'):
            oneshot_rules[self.name] = self
            pyglet.clock.schedule_interval(self.schedule_once,self.period)   # infinite loop
        else:
            rules[self.name] = self
        print ":: new rule :", self.name, self.actors
        self.setup()

    def setup(self):
        pass

    def tick(self,dt, actor):  # this is the method that defines the action
        pass

    def schedule_once(self,dt):
        oneshot_rules[self.name] = self

    # PROBLEM with image export that does not use pyglet clock
##--- MOVE RULES --------------------------------------------------------------
# replace with general OpenGL? matrix transform : see euclid.py                 TODO

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
#                                                                               TODO
# following rules need a vector, point, and derivatives
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
        if (c.peg.x + c.aabb.lox < self.rect.lox
                or c.aabb.hix + c.peg.x > self.rect.hix):
            # if bounce, reverse speed and move once
            c.peg = c.peg._replace(
                    x = c.peg.x - c.vel.vx * dt,
                    y = c.peg.y + c.vel.vy * dt)
            c.vel = c.vel._replace(vx = c.vel.vx * -1.0)
            publish('BUMP', c.name)
            # self.shape.color = choice(kapla_colors)      # change clr
        elif (c.peg.y + c.aabb.loy < self.rect.loy
                or c.aabb.hiy + c.peg.y > self.rect.hiy):
            c.peg = c.peg._replace(
                    x = c.peg.x + c.vel.vx * dt,
                    y = c.peg.y - c.vel.vy * dt)
            c.vel = c.vel._replace(vy = c.vel.vy * -1.0)
            publish('BUMP', c.name)
        else :
            pass

class Wrap(Rule):
    def tick(self, dt, actor):  # exits and reenters the Rect the oposite side
        pass

class Cycle_Color(Rule):
    def setup(self):
        self.i = cycle(self.color_list)

    def tick(self, dt, a):
        print ':: cycling color'
        shapes.lmnts[a.shape].color = self.i.next()
        shapes.lmnts[a.shape].batch = None

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
    for rulename in oneshot_rules:
        for actor in oneshot_rules[rulename].actors:
            oneshot_rules[rulename].tick(dt, cast[actor])
        del oneshot_rules[rulename]

    for rulename in rules:
        for actor in rules[rulename].actors:
            rules[rulename].tick(dt, cast[actor])

    for rulename in conditional_rules:
        for actor in rules[rulename].actors:
            if rules[rulename].prerequisite in _events:
                rules[rulename].tick(dt, cast[actor])
            else:
                pass

    #events._events = {}
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


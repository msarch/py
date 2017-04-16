#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev109
'''

##--- IMPORTS -----------------------------------------------------------------
from collections import defaultdict
import weakref
from itertools import cycle
import pyglet
import shapes
##--- CONSTANTS AND VARIABLES -------------------------------------------------

##--- RULE CLASS --------------------------------------------------------------
class Rule(object):
    __oneshot__ = defaultdict(list)
    __persistent__ = defaultdict(list)
    __conditional__ = defaultdict(list)

    def __init__(self,name="no name", **kwargs):
        self.name=name
        for i in kwargs:
            setattr(self,i,kwargs[i])

        if hasattr(self, 'period'):
            self.__oneshot__[self.__class__].append(weakref.ref(self))
            pyglet.clock.schedule_interval(self.schedule_once,self.period)   # infinite loop

        elif hasattr(self, 'condition'):
            self.__conditional__[self.__class__].append(weakref.ref(self))
            pyglet.clock.schedule_interval(self.schedule_once,self.period)

        else:
            self.__persistent__[self.__class__].append(weakref.ref(self))

        print ":: new rule :", self.name, self.groups
        self.setup()

    def setup(self):
        pass

    def tick(self,dt, group):  # this is the method that defines the action
        pass


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
    def tick(self, dt, group):
        self.shape.peg = self.shape.peg._replace(
                angle = self.shape.peg.angle + self.av * dt)
#                                                                               TODO
# following rules need a vector, point, and derivatives
# i.e. speed vector, angular velocity or matrix
# attached to the shape itself and no more to the rule.
# ex : avoid pb BETWEEN rules : bounce
class Cruise(Rule):  # heads to a direction (angle) forever
    def tick(self, dt, group):
        pass

class Head_to(Rule):
    def tick(self, dt, group):  # goes towards the head_to point and beyond
        pass

class Look_at(Rule):
    def tick(self, dt, group):  # orients itself towards the look_at point
        pass

class Walk_path(Rule):
    def tick(self, dt, group):  # exits and reenters the Rect the oposite side
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
    def tick(self, dt, group):  # exits and reenters the Rect the oposite side
        pass

class Cycle_Color(Rule):
    def setup(self):
        self.i = cycle(self.color_list)

    def tick(self, dt, a):
        print ':: cycling color'
        a.shapes.color = self.i.next()
        a.shapes.batch = None
# remember to erase batch if shape has changed : make a color setter in shape  : TODO

##--- META RULES --------------------------------------------------------------
# meta rules are given a rule name as argument
# other rules can have their parameters modified, deleted, reordered

class Lifespan(Rule):
    def tick(self, dt, group):
        ''' Timetable or scenario class
        - keeps track for every rule of a start and end time for each group
        - can be dict read from text file
        '''
        pass

class Visible(Rule):
    def tick(self, dt, group):
        ''' Timetable or scenario class
        - keeps track for every rule of a start and end time for each group
        - can be dict read from text file
        '''
        pass


#--- FUNCS --------------------------------------------------------------------
def tick(dt):
    ## LATER SIMPLIFICATION : alll rules should be gathered and ORDERED by some way
    ## then 'conditional' could be ordered first, etc.... 'draw' and 'export' last
    #for rulename in conditional_rules:
        ## goes first because conditions come from previous generation
        #for group in rules[rulename].groups:
            #if rules[rulename].prerequisite in _events:
                #rules[rulename].tick(dt, group)
            #else:
                #pass

    #for rulename in oneshot_rules:
        ## executed and immediatly deleted
        #for group in oneshot_rules[rulename].groups:
            #oneshot_rules[rulename].tick(dt, group)
        #del oneshot_rules[rulename]

    #for rulename in rules:
    ## come last because rules change conditions fro next gen
    ## i.e. publish or broadcast new information
        #for group in rules[rulename].groups:
            #rules[rulename].tick(dt, group)

    ## and draw ASAP after changes
    #shapes.get_batch()
    #shapes.draw()

    #events._events = {}
    pass

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


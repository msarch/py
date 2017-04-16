#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * dec 2014 * bw-rev113
'''

##--- IMPORTS -----------------------------------------------------------------
from itertools import cycle
from rules import Rule, broadcast

# PROBLEM with image export that does not use pyglet clock
##--- MOVE RULES --------------------------------------------------------------
# replace with general OpenGL? matrix transform : see euclid.py                 TODO

class Slide(Rule):
    def tick(self, dt):  # simple dx and dy displacement
        for sh in self._items:
            sh.peg = sh.peg._replace(
                x = sh.peg.x + sh.vel.vx * dt,
                y = sh.peg.y + sh.vel.vy * dt,
                angle = sh.peg.angle)

class Spin(Rule):
    def tick(self, dt):
        for sh in self._items:
            sh.peg = sh.peg._replace(angle = sh.peg.angle + self.av * dt)
#                                                                               TODO
# following rules need a vector, point, and derivatives
# i.e. speed vector, angular velocity or matrix
# attached to the shape itself and no more to the rule.
# ex : avoid pb BETWEEN rules : bounce
class Cruise(Rule):  # heads to a direction (angle) forever
    def tick(self, dt):
        pass

class Head_to(Rule):
    def tick(self, dt):  # goes towards the head_to point and beyond
        for sh in self._items:
            pass

class Look_at(Rule):
    def tick(self, dt):  # orients itself towards the look_at point
        for sh in self._items:
            pass

class Walk_path(Rule):
    def tick(self, dt):  # exits and reenters the Rect the oposite side
        for sh in self._items:
            pass

##--- COLLISION RULES ---------------------------------------------------------
class Bounce(Rule):
    def tick(self, dt):
        for c in self._items:
            if (c.peg.x + c.aabb.lox < self.box.lox
                    or c.aabb.hix + c.peg.x > self.box.hix):
                # if bounce, reverse speed and move once
                c.peg = c.peg._replace(
                        x = c.peg.x - c.vel.vx * 2 * dt, # *2 to avoid sticking
                        y = c.peg.y + c.vel.vy * 2 * dt) # to the border
                c.vel = c.vel._replace(vx = c.vel.vx * -1.0)
                broadcast('BUMP-X', c)
            elif (c.peg.y + c.aabb.loy < self.box.loy
                    or c.aabb.hiy + c.peg.y > self.box.hiy):
                c.peg = c.peg._replace(
                        x = c.peg.x + c.vel.vx * 2 * dt,
                        y = c.peg.y - c.vel.vy * 2 * dt)
                c.vel = c.vel._replace(vy = c.vel.vy * -1.0)
                broadcast('BUMP-Y', c)
            else :
                pass

class Wrap(Rule):
    def tick(self, dt):  # exits and reenters the Rect the oposite side
        for sh in self._items:
            pass

class Cycle_Color(Rule):
    def setup(self):
        self.i = cycle(self.color_list)
        self.t = cycle(self.targets)
    def tick(self, dt):
        t = self.t.next()
        i = self.i.next()
        t.color = i
        print ':: cycling color',t,i,
        t.batch=None
# remember to erase batch if shape has changed or make a color setter in shape  TODO

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


 #----------------------------------------------------------------------------- NOTES
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
'''


#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * jan 2015 * bw-rev113
'''

##--- IMPORTS -----------------------------------------------------------------
from itertools import cycle
from actions.agent import Action, broadcast

# PROBLEM with image export that does not use pyglet clock
##--- MOVE RULES --------------------------------------------------------------
# replace with general OpenGL? matrix transform : see euclid.py                 TODO



class Spin(Action):
    def tick(self, dt):
        for sh in self.targets:
            sh.peg = sh.peg._replace(angle = sh.peg.angle + self.av * dt)
#                                                                               TODO
# following actions need a vector, point, and derivatives
# i.e. speed vector, angular velocity or matrix
# attached to the shape itself and no more to the agent.
# ex : avoid pb BETWEEN actions : bounce
class Cruise(Action):  # heads to a direction (angle) forever
    def tick(self, dt):
        pass

class Head_to(Action):
    def tick(self, dt):  # goes towards the head_to point and beyond
        for sh in self._items:
            pass

class Look_at(Action):
    def tick(self, dt):  # orients itself towards the look_at point
        for sh in self._items:
            pass

class Walk_path(Action):
    def tick(self, dt):  # exits and reenters the Rect the oposite side
        for sh in self._items:
            pass

##--- COLLISION RULES ---------------------------------------------------------
class Wrap(Action):
    def tick(self, dt):  # exits and reenters the Rect the oposite side
        for sh in self.targets:
            pass

# remember to erase batch if shape has changed or make a color setter in shape  TODO

##--- META RULES --------------------------------------------------------------
# meta actions are given a agent name as argument
# other actions can have their parameters modified, deleted, reordered

 #----------------------------------------------------------------------------- NOTES
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
'''


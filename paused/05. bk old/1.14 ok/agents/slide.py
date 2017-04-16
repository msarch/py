#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * jan 2015 * bw-rev113
'''

##--- IMPORTS -----------------------------------------------------------------
from agents.agent import Agent, broadcast

# PROBLEM with image export that does not use pyglet clock
##--- MOVE RULES --------------------------------------------------------------
# replace with general OpenGL? matrix transform : see euclid.py                 TODO

class Slide(Agent):
    def tick(self, dt):  # simple dx and dy displacement
        for sh in self._items:
            sh.peg = sh.peg._replace(
                x = sh.peg.x + sh.vel.vx * dt,
                y = sh.peg.y + sh.vel.vy * dt,
                angle = sh.peg.angle)

slide = Slide

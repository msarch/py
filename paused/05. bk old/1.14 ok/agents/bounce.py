#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# msarch@free.fr * jan 2015 * bw-rev113

##--- IMPORTS -----------------------------------------------------------------
from agents.agent import Agent, broadcast

# PROBLEM with image export that does not use pyglet clock
##--- MOVE RULES --------------------------------------------------------------
# replace with general OpenGL? matrix transform : see euclid.py                 TODO

##--- COLLISION RULES ---------------------------------------------------------
class Bounce(Agent):
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

bounce = Bounce

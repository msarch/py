#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# msarch@free.fr * jan 2015 * bw-rev113

##--- IMPORTS -----------------------------------------------------------------
from engine.agent import Agent

# PROBLEM with image export that does not use pyglet clock
##--- MOVE RULES --------------------------------------------------------------
# replace with general OpenGL? matrix transform : see euclid.py                 TODO

##--- COLLISION RULES ---------------------------------------------------------
class Bounce(Agent):
    def tick(self, dt):
        for sh in self.targets:
            if (sh.peg.x + sh.aabb.lox < self.box.lox
                    or sh.aabb.hix + sh.peg.x > self.box.hix):
                # if bounce, reverse speed and move once
                sh.peg = sh.peg._replace(
                        x = sh.peg.x - sh.vel.vx * 2 * dt, # *2 to avoid sticking
                        y = sh.peg.y + sh.vel.vy * 2 * dt) # to the border
                sh.vel = sh.vel._replace(vx = sh.vel.vx * -1.0)
                self.broadcast(self.message, sh)
            elif (sh.peg.y + sh.aabb.loy < self.box.loy
                    or sh.aabb.hiy + sh.peg.y > self.box.hiy):
                sh.peg = sh.peg._replace(
                        x = sh.peg.x + sh.vel.vx * 2 * dt,
                        y = sh.peg.y - sh.vel.vy * 2 * dt)
                sh.vel = sh.vel._replace(vy = sh.vel.vy * -1.0)
                self.broadcast(self.message, sh)
            else :
                pass

bounce = Bounce

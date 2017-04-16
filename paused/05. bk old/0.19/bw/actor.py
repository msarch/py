#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 19 :: 03.2014 :: msarch@free.fr

##---IMPORTS-------------------------------------------------------------------
import pyglet.gl
from debug import db_print


##---CLASS ACTOR---------------------------------------------------------------
class Actor(object):
    "Stores the position, orientation, shape, rule of an actor"
    count = 1
    def __init__(self, shape=None, anchorx=0.0, anchory=0.0, angle=0.0,
            drawable=True, layer=0, rules=[], **kwargs):
        self.shape = shape
        self.anchorx = anchorx
        self.anchory = anchory
        self.angle = angle
        self.drawable = drawable
        self.layer = layer
        self.rules = rules
        self.nume = Actor.count
        Actor.count+=1

    def tick(self, dt):
        # TODO for rules in self.rules
        print 'actor', self.nume, 'tick not implemented'
        print self.rules

    def paint(self):
        if self.shape:
            if self.drawable:
                pyglet.gl.glPushMatrix()
                pyglet.gl.glTranslatef(self.anchorx, self.anchory, 0)
                pyglet.gl.glRotatef(self.angle, 0, 0, 1)
                batch = self.shape.get_batch()
                batch.draw()
                pyglet.gl.glPopMatrix()
                db_print (self.nume, 'drawn')
            else:
                print 'actor', self.nume, 'not drawn'
        else:
            print 'actor', self.nume, 'has no shape'

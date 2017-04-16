#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/actor :: rev 20 :: MAY2014 :: msarch@free.fr

##---IMPORTS-------------------------------------------------------------------
import pyglet.gl
from debug import db_print
import debug


##---CLASS ACTOR---------------------------------------------------------------
class Actor(object):
    "Stores the position, orientation, shape, rule of an actor"
    count = 0
    registry=[]

    def __init__(self, shape=None, ruleset=[], anchorx=0.0, anchory=0.0, angle=0.0,
            drawable=True, layer=0, **kwargs):
        self.shape = shape
        self.anchorx = anchorx
        self.anchory = anchory
        self.angle = angle
        self.drawable = drawable
        self.layer = layer
        self.ruleset = ruleset
        Actor.count+=1
        self.nume = Actor.count
        Actor.registry.append(self)
        db_print( 'actor #',self.nume,'added to scene', self)
        db_print('ruleset is :', self.ruleset,'shape is:', self.shape)

    def tick(self, dt):
        # TODO for rules in self.rules
        for rule in self.ruleset:
            rule(self,dt)
        db_print('rules for actor number:', self.nume, self.ruleset)

    def paint(self,dt):
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

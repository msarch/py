#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 17 :: 03.2014 :: msarch@free.fr

##---IMPORTS-------------------------------------------------------------------
import os
import pyglet.gl
from glob import glob
from imp import load_source
from engine18 import Engine


##---CLASS ACTOR---------------------------------------------------------------
class Actor(object):
    "Stores the position, orientation, shape, rule of an actor"
    def __init__(self, shape=None, anchor=(0, 0), angle=0, drawable=True,
            layer=0, rules=[], **kwargs):
        self.shape = shape
        self.anchor = anchor
        self.angle = angle
        self.drawable = drawable
        self.layer = layer
        self.rules= rules

    def tick(self, dt):
        # TODO for rules in self.rules
        print self, 'tick not implemented'
        print self.rules

    def paint(self):
        if self.shape:
            print self, self.shape
            if self.drawable:
                pyglet.gl.glPushMatrix()
                pyglet.gl.glTranslatef(self.anchor[0], self.anchor[1], 0)
                pyglet.gl.glRotatef(self.angle, 0, 0, 1)
                batch = self.shape.get_batch()
                batch.draw()
                pyglet.gl.glPopMatrix()
            print self, 'not drawn'
        print self, 'has no shape'

#-CLASS SCENE------------------------------------------------------------------
class Scene(object):
    ''' Stores a list of actors, rotation and shape of an actor '''
    def __init__(self, folder=None):
        self.folder = folder
        self.actor_registry = []
        self.get_actors()

    #---dynamic scene handling ------------------------------------------------
    def get_actors(self):
        for path in glob('scene/[!_]*.py'):
            name, ext = os.path.splitext(os.path.basename(path))
            mdl = load_source(name, path)
        if hasattr(mdl, 'register'):
            self.actor_registry.append(mdl.register())

    def add(self, actor):
        self.actor_registry.append(actor)

    def tick(self, dt):
        print self, 'tick...'
        for actor in self.actor_registry:
            actor.tick(actor, dt)

    def paint(self):
        print self, 'paint...'
        for actor in self.actor_registry:
            actor.paint()


##---MAIN----------------------------------------------------------------------
def main():
    s = Scene(folder='scene')
    e = Engine(s, duration=7)
    e.run()


##-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

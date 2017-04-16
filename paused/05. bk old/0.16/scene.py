!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: scene :: rev 16 :: 02.2014 :: msarch@free.fr

import os

from pyglet.gl import *
from glob import glob
from imp import load_source

#--- FUNCTIONS ----------------------------------------------------------------

class Actor(object):
    "Stores the coordinates and shape of an actor"

    def __init__(self, shape=None,anchor=(0,0),angle=0, drawable=True,**kwargs):
        self.shape = shape
        self.anchor=anchor
        self.angle=angle
        self.drawable = drawable

    def tick(self,dt):
        print 'tick...'

    def paint(self):
        glPushMatrix()
        glTranslatef(self.anchor[0],self.anchor[1], 0)
        glRotatef(self.angle, 0, 0, 1)
        batch = self.shape.get_batch()
        batch.draw()
        glPopMatrix()

class Scene(object):
    "Collects all actors in scene folder"

    def __init__(self, folder='', duration=0):
        self.actor_register = []
        self.folder = folder
        self.duration = duration

    def tick(self,dt):
        for actor in self.actor_register:
            actor.tick(dt)

    def paint(self):
        for actor in self.actor_register:
            actor.paint()

    def configure(self):
        #import all py files in self.folder
        os.chdir(self.folder)
        for filename in glob("*.py"):
            curdir = os.path.dirname(os.path.abspath(__file__))
            mysubdir= "/".join((curdir,self.folder))
            actor_file= "/".join((mysubdir,filename))
            new_actor = load_source(filename,actor_file)
            if hasattr(new_actor, 'register'):
                self.actor_register.append(new_actor.register())




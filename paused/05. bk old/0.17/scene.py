#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 17 :: 03.2014 :: msarch@free.fr

##---IMPORTS-------------------------------------------------------------------

import os
from glob import glob
from imp import load_source


##---CONSTANTS AND VARIABLES---------------------------------------------------
class Actor(object):
    "Stores the coordinates and shape of an actor"

    def __init__(self, shape=None,anchor=(0,0),angle=0, drawable=True, priority=0,**kwargs):
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

    def __init__(self, folder=None):
        self.folder_name=folder
        self.fl=[] # file list
        self.actor_registry = []
        self.rule_registry = []

        get_file_list(folder)
        get_actors(fl)
        get_global_rules(fl)

    #---dynamic scene handling ------------------------------------------------

    def get_file_list(self,folder):


    def get_actors(self,file_list  ):
        #import all py files in self.scene_folder
        for filename in glob("*.py"):
            next_file= os.path.join((self.folder_path,filename))
            new_actor = load_source(filename,next_file)
            if hasattr(new_actor, 'register'):
                self.actor_registry.append(new_actor.register())

    def get_global_rules(self):
        os.chdir(self.folder)
        for filename in glob("*.py"):
            next_file= os.path.join((self.folder_path,filename))
            new_rule = load_source(filename,next_file)
            if hasattr(new_rule, 'global_rule'):
                self.rule_registry.append(new_rule.register())


    def withdraw_actor(self,actor):
        pass

    def add_actor(self,actor):
        pass

    def paint(self):
        for actor in self.actor_registry:
            actor.paint()

    def tick(self):
        for actor in self.actor_registry:
            actor.tick()
_____________________________________________________________________

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

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 19 :: 03.2014 :: msarch@free.fr

##---IMPORTS-------------------------------------------------------------------
import os
from glob import glob
from imp import load_source
from debug import db_print


#-CLASS SCENE------------------------------------------------------------------
class Scene(object):
    ''' Stores a list of actors, rotation and shape of an actor '''
    def __init__(self, folder=None):
        self.folder = folder
        self.actor_registry = []  # TODO : make it a dict with module names?
        self.get_actors()

    #---dynamic scene handling ------------------------------------------------
    def get_actors(self):
        db_print('getting modules from :',self.folder)
        for path in glob(self.folder+'/[!_]*.py'):
            db_print('trying to load :',path)
            name, ext = os.path.splitext(os.path.basename(path))
            mdl = load_source(name, path)
            db_print (mdl, 'is loaded')

            if hasattr(mdl, 'register'):
                self.actor_registry.extend(mdl.register())
                # register should return A LIST with one or multiple actors

    def add(self, actor):
        self.actor_registry.append(actor)

    def tick(self, dt):
        db_print ('SCENE TICK')
        for actor in self.actor_registry:
            actor.tick(actor, dt)

    def paint(self):
        db_print ('SCENE PAINT')
        for actor in self.actor_registry:
            actor.paint()

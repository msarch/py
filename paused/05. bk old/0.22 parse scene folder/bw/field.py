#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/actor :: rev 22 :: MAY2014 :: msarch@free.fr

##---IMPORTS-------------------------------------------------------------------
import os
import sys
import inspect

from glob import glob
from imp import load_source
import pyglet.gl
import records
from debug import db_print

##--- CONSTANTS AND VARIABLES -------------------------------------------------
DEFAULT_SCENE_FOLDER ='scene'  #  should be at same path level as main folder


##---CLASS ACTOR---------------------------------------------------------------
class Actor(object):
    "Stores the position, orientation, shape, rule of an actor"

    def __init__(self,
            shape=None,
            ruleset=[],
            anchorx=0.0,
            anchory=0.0,
            angle=0.0,
            drawable=True,
            layer=0,
            **kwargs):
        self.shape = shape
        self.anchorx = anchorx
        self.anchory = anchory
        self.angle = angle
        if self.shape:
            self.drawable = drawable
        else:
            self.drawable= False
        self.layer = layer
        self.ruleset = ruleset
        Field.add_actor(self)

    def tick(self, dt):
        # TODO for rules in self.rules
        for rule in self.ruleset:
            rule(self,dt)

    def paint(self):
        if self.shape:
            if self.drawable:
                pyglet.gl.glPushMatrix()
                pyglet.gl.glTranslatef(self.anchorx, self.anchory, 0)
                pyglet.gl.glRotatef(self.angle, 0, 0, 1)
                batch = self.shape.get_batch()
                batch.draw()
                pyglet.gl.glPopMatrix()
            else:
                print 'actor', self, 'not drawn'
        else:
            print 'actor', self, 'has no shape'


##---ACTORS FOLDER PARSING-----------------------------------------------------
class Field():

    @staticmethod
    def init():
        Field.registry=[]
        scene_folder=Field.get_scene_folder()
        Field.parse_folder(scene_folder)
        db_print(records.SIZE)

    @staticmethod
    def get_scene_folder():
        ''' returns the folder specified by the user
        '''
        if len(sys.argv) == 2:
            fn = sys.argv[1]
            # TODO : use getopt?
            db_print ('user folder is :',fn)
            if os.path.exists(fn):
                db_print (os.path.basename(fn),'exists')  # file exists
                return(fn)
            else:
                exit()
        else:  # default scene folder in main folder
            fn = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..',
                DEFAULT_SCENE_FOLDER ))
            db_print ('user folder is :',fn)
            return(fn)

    @staticmethod
    def parse_folder(scene_folder):
        ''' Loads al module inside scene_folder
        '''
        db_print('getting modules from :',scene_folder)

        sys.path.insert(0,scene_folder)  # include scene folder

        for path in glob(scene_folder+'/[!_]*.py'):
            db_print('trying to load :',path)
            name, ext = os.path.splitext(os.path.basename(path))
            mdl = load_source(name, path)
            db_print (name, 'is loaded')
            db_print (mdl)

    @staticmethod
    def tick(dt):
        # TODO for rules in self.rules
        for actor in Field.registry:
            for rule in actor.ruleset:
                rule(actor,dt)

    @staticmethod
    def paint():
        print Field.registry
        for actor in Field.registry:
            actor.paint()

    @staticmethod
    def add_actor(actor):
        Field.registry.append(actor)
        db_print( 'actor #',actor,'added to Field')
        db_print('ruleset is :', actor.ruleset,'shape is:', actor.shape)


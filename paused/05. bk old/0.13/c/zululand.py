#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus: :: rev 13-c :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------

from pyglet import clock
import display

##  CONSTANTS AND VARIABLES ---------------------------------------------------

##--- LAND -------------------------------------------------------------------

class Land(object):

    def __init__(self,size,color):
        self.zulus=[]
        self.ruleset=[]
        self.size=size
        self.color=color
        # schedule the update function, 60 times per second
        clock.schedule_interval(self.update, 1.0/120.0)

    def update(self,dt):
        for r in Rule:
            r.update(dt)
        print 'updating...'

    def draw(self):
        for z in Zulu:
            print 'zulu :', z
            print 'shape: ', z.shape
            print 'position:', z.position
            print 'color:', z.color
            z.shape.draw(z.position,z.color)

##--- ZULUS -------------------------------------------------------------------

class MakeMeIterable(type):
    def __iter__(cls):
        return iter(cls._registry)

class Zulu(Land):
    """ Zulus objects themselves are merely identifiers of canvas entities.
    They do not contain any data themselves other than an entity id.
    Entities must be instantiated, constructor arguments can be
    specified arbitarily by the subclass.
    """
    __metaclass__ = MakeMeIterable
    _registry = []

    def __init__(self,shape=None,position=[0,0,0],\
            color=[255.0,255.0,255.0,0.0]):
        self._registry.append(self)
        self.shape=shape
        self.position=position
        self.color=color
        print 'zulu init -->', self



#--- RULES --------------------------------------------------------------------

class Rule(Land):
    __metaclass__ = MakeMeIterable
    _registry = []

    def __init__(self):
        self._registry.append(self)
        self.zulus=[]

    def add(self,*args):
        """ adds one or more zulus to the rule pool
        """
        for z in args:
            self.zulus.append(z)

    def list(self):
        """ list of zulus or zulus args? concerned by the rule
        """
        pass

#--- FUNCTIONS ----------------------------------------------------------------


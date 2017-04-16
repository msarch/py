#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus: :: rev 13-d :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
import pygtools
import pyglet
import itertools
##  CONSTANTS AND VARIABLES ---------------------------------------------------

class Land(object):

    def __init__(self,size,fps,color):
        self.size=size
        self.color=color
        self.paused=False
        _=pygtools.PygletViewport(self)

    def run(self):
        pyglet.app.run()

    def update(self,dt):
        """iterate through rules and apply them to everyone concerned
        """
        for rule in Rule:
            for zulu in rule.zulus:
                rule.apply(zulu,dt)
    #  merged = list(itertools.chain.from_iterable(Rule))

    def draw(self):
        """iterate through zulu shapes and draw them
        """
        for z in Zulu:
            z.shape.draw(z.position,z.color)

##--- ZULUS -------------------------------------------------------------------

class MakeMeIterable(type):
    def __iter__(cls):
        return iter(cls._registry)

class Zulu(object):
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


#--- RULES --------------------------------------------------------------------

class Rule(object):
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





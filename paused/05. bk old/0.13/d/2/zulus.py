#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus: :: rev 13-d2 :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
import itertools
from pyglet.gl import *

##  CONSTANTS AND VARIABLES ---------------------------------------------------

##--- ZULU CLASS --------------------------------------------------------------

tribe=[]

class Zulu(object):
    """ Zulus objects themselves are merely identifiers of canvas entities.
    They do not contain any data themselves other than an entity id.
    Entities must be instantiated, constructor arguments can be
    specified arbitarily by the subclass.
    """


    def __init__(self,shape=None,position=[0,0,0],angle=0,\
            color=[255.0,255.0,255.0,0.0],drawable=True):
        tribe.append(self)
        self.shape=shape
        self.x,self.y,self.z=position
        self.color=color
        self.angle=angle
        self.drawable=drawable

#--- FUNCTIONS ----------------------------------------------------------------

def render_all():

    for z in itertools.ifilter(lambda z : z.drawable,tribe):
        glPushMatrix()
        glTranslatef(z.x,z.y,z.z)   # Move back
        glRotatef(z.angle, 0, 0, 1)
        gl.glColor4f(*z.color)
        z.shape.draw()
        glPopMatrix()

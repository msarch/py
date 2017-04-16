#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus: :: rev 13-d3 :: 10.2013 :: msarch@free.fr

##  TO DO LIST ----------------------------------------------------------------
# TODO ANCHORS
# bodys have an anchor to which displacements are applied

# TODO : ZULU CLASS
# anchor point and rot(or align-to  or look-at point) are zulu level,
# colors + linestyle are bodys (superclass) level
# zulus have a set of points
#   - one (number 0) is anchor
#   - others are geom(4 for recs, 3 for tri, 2 for lines etc..,
#   - extras are 'pegs' to anchor other geometries thus NO GROUPS are needed

# TODO : GROUPS
# implement groups similar to nobgl layers


##  IMPORTS -------------------------------------------------------------------
import itertools
import collections
from pyglet.gl import *

##  CONSTANTS AND VARIABLES ---------------------------------------------------

##--- ZULU CLASS --------------------------------------------------------------


class Zulu(object):
    """ Zulus objects themselves are merely identifiers of canvas entities.
    They do not contain any data themselves other than an entity id.
    Entities must be instantiated, constructor arguments can be
    specified arbitarily by the subclass.
    - position GPU managed
    - rotation because GPU managed
    - no acceleration, CPU managed only in custom rules field
    """
# FIXME ^^^

# - zulus are NOT bodys, zulus may have bodys, one or a group
# - zulus may generate bodys, or fields or values
# - zulus live ie : perform actions
    tribe=[]

    def __init__(self,body=None,anchor=[0,0],angle=0,\
            color=[255.0,255.0,255.0,0.0],drawable=True):
        Zulu.tribe.append(self)
        self.body=body
        self.anchor=anchor
        self.angle=angle
        self.drawable=drawable

#--- FUNCTIONS ----------------------------------------------------------------

def paint_all():
    for z in Zulu.tribe:
        glPushMatrix()
        glTranslatef(z.anchor[0],z.anchor[1],0)   # Move bac
        glRotatef(z.angle, 0, 0, 1)
        z.body.batch_draw()
        glPopMatrix()



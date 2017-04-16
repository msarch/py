#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus: :: rev 13-b :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
##  CONSTANTS AND VARIABLES ---------------------------------------------------
##--- ZULUS CLASS -------------------------------------------------------------

class Zulu(object):
    """ Zulus objects themselves are merely identifiers of canvas entities.
    They do not contain any data themselves other than an entity id.
    Entities must be instantiated, constructor arguments can be
    specified arbitarily by the subclass.
    """
    nation=[]

    def __init__(self):

        #this makes Zulu iterable
        self.nation.append(self)

        self.shape=None #shape
        self.centroid=None #point
        self.color=None #color

    def draw(self):
        self.shape.draw(self.centroid,self.color)







#--- FUNCTIONS ----------------------------------------------------------------






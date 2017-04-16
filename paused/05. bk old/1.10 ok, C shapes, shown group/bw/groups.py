#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev109
'''

#--- IMPORTS ------------------------------------------------------------------
from collections import OrderedDict
from collections import defaultdict
import weakref
import shapes
from utils import cfg
#from vector import Vec2

##--- CONSTANTS AND VARIABLES -------------------------------------------------

##--- Group class --------------------------------------------------------------
class Group(object):

    __refs__ = defaultdict(list)

    def __init__(self, name="no name", **kwargs):
        self.__refs__[self.__class__].append(weakref.ref(self))
        self.name=name
        for i in kwargs:
            setattr(self,i,kwargs[i])
        print ":: new group :", self.name

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            # if is a group --> chain
            # l2 = list(itertools.chain.from_iterable(list_of_lists))
            inst = inst_ref()
            if inst is not None:
                yield inst

    @classmethod
    def get_drawables(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                if inst.drawable:
            # use : list(itertools.ifilter(lambda x: x % 2, numbers))
                    yield inst


##--- groups module paint func -------------------------------------------------
#    @property
    #def pos(self):
        #return (self.peg.x, self.peg.y, self.peg.angle)

    #@pos.setter
    #def peg(self, new_pg):
        #self._peg = (new_pg)

    #@property
    #def vel(self):
        #return (self._vx, self._vy, self._av)

    #@vel.setter
    #def vel(self,new_vel):
        #self._vx *= (value/self.speed)
        #self._vy *= (value/self.speed)

    #@property
    #def speed(self):
        #return ((dx**2 + dy**2) *0.5)

#class Temperature( object ):
    #def fget( self ):
        #return self.celsius * 9 / 5 + 32
    #def fset( self, value ):
        #self.celsius= (float(value)-32) * 5 / 9
    #farenheit= property( fget, fset )
    #def cset( self, value ):
        #self.cTemp= float(value)
    #def cget( self ):
        #return self.cTemp
    #celsius= property( cget, cset, doc="Celsius temperature" )


    #def __str__(self):
        #return 'Point: x=%6.3f y=%6.3f hypot=%6.3f' \
                #% (self.x, self.y, self.hypot)


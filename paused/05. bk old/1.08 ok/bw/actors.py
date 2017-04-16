#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev108
'''

#--- IMPORTS ------------------------------------------------------------------
from collections import OrderedDict
import shapes
from utils import cfg
#from vector import Vec2

##--- CONSTANTS AND VARIABLES -------------------------------------------------
cast = OrderedDict()


##--- actor class --------------------------------------------------------------
class Actor(object):

    def __init__(self, name, **kwargs):
        global cast
        if name in cast:
            raise ValueError('duplicate actor name', name)
            exit(1)
        elif name == '':
            raise ValueError('no actor name', name)
        else:
            self.name=name
        cast[self.name] = self
        print ":: new actor :", self.name
        for i in kwargs:
            setattr(self,i,kwargs[i])
        if not hasattr(self,'peg'):  # peg must be tuple (x, y, a)
            self.peg = cfg.DOCKED
        if not hasattr(self,'vel'):  # peg must be tuple (vx, vy, av)
            self.vel = cfg.IDLE
        self.aabb = shapes.lmnts[self.shape].get_aabb()


##--- actors module paint func -------------------------------------------------
def paint():
    print 'p :',
    for actor in cast:
        if hasattr(cast[actor],'shape'):
        # paint()  can be called for shape as well as for compound_shapes
        # as both classes have the method
        # check if paint method can be unified                                # TODO
            print cast[actor].shape,
            shapes.lmnts[cast[actor].shape].paint(cast[actor].peg)
        else:
            pass
    print ''

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


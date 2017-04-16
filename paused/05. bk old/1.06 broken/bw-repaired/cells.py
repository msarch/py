#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev106
'''

#--- IMPORTS ------------------------------------------------------------------
from utils import cfg
from collections import OrderedDict
import shapes
#from vector import Vec2

##--- CONSTANTS AND VARIABLES -------------------------------------------------
lmnts = OrderedDict()
lmnts['a'] = 'A'

##---GENERAL GRAPHIC shape CLASS-----------------------------------------------
class Cell(object):

    def __init__(self, name, **kwargs):
        global lmnts
        if name in lmnts:
            raise ValueError('duplicate cell name', name)
            exit(1)
        elif name == '':
            raise ValueError('no cell name', name)
        else:
            self.name=name

        lmnts[self.name] = self
        print lmnts

        for i in kwargs:
            setattr(self,i,kwargs[i])

        if not hasattr(self,'peg'):  # peg must be (x, y, a)
            self.peg = cfg.DOCKED

#       #if not hasattr(self,'speed'):  # peg must be (x, y, a)
            #self.vel1 = IDLE

        print ""
        print ":: new cell, cfg.lmnts is now :"
        print lmnts
        for r in lmnts:
            print""
            print 'cell :', r
            print lmnts[r]



def paint():
    for cell in lmnts:
        if hasattr(lmnts[cell],'shape'):
        # paint()  can be called for shape as well as for compound_shapes
        # as both classes have the method
        # check if paint method can be unified                                # TODO
            print 'painting cell shape', lmnts[cell].shape
            shapes.lmnts[lmnts[cell].shape].paint(lmnts[cell].peg)
        else:
            pass


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


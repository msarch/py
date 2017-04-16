#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev106
'''

#--- IMPORTS ------------------------------------------------------------------
from collections import OrderedDict
#from vector import Vec2

##--- CONSTANTS AND VARIABLES -------------------------------------------------
lmnts = OrderedDict()
print lmnts
print' ************************inited'
lmnts['a'] = 'A'

##---GENERAL GRAPHIC shape CLASS-----------------------------------------------
class Cell(object):

    def __init__(self, name):
        global lmnts
        self.name=name
        lmnts[self.name] = self
        print ":: new cell, cfg.lmnts is now :", lmnts



def paint():
    print ''
    print ' cfg.lmnts seen from paint_all() classmethod :', lmnts

    for cell in lmnts:
        print cell



#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev107 * striped down
'''

#--- IMPORTS ------------------------------------------------------------------
from collections import OrderedDict
#from vector import Vec2

##--- CONSTANTS AND VARIABLES -------------------------------------------------
set = OrderedDict()
set['bar'] = 'foo'

##---GENERAL GRAPHIC shape CLASS-----------------------------------------------
class Cell(object):

    def __init__(self, name, **kwargs ):
        global set
        self.name=name
        set[self.name] = self
        print "set @cells/init :", set


def paint():
    for cell in set:
        print 'painting cell :', cell
        print ' set is accessible from cells/Cell/paint'


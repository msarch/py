#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev105
'''

#--- IMPORTS ------------------------------------------------------------------
from itertools import chain
from collections import namedtuple


##--- CONSTANTS AND VARIABLES -------------------------------------------------
Point  = namedtuple('Point', 'x y')
Rect   = namedtuple('Rect', 'lox loy hix hiy')
AABB   = namedtuple('AABB', Rect._fields)
Speed  = namedtuple('Speed','vx vy av')
Speed1 = namedtuple('Speed1', 'speed heading')
Speed2 = namedtuple('Speed2', 'x y angle speed')
Peg    = namedtuple('Peg','x y angle')
Peg2   = namedtuple('Peg2', 'x y angle speed head_to') # or use Peg3 ??
Peg3   = namedtuple('Peg3', 'x y angle speed path') # target
Set    = namedtuple('set', 'rulename rule_args subject')

ORIGIN = Point(0.0, 0.0)
IDLE   = Speed(0.0, 0.0, 0.0)
DOCKED = Peg(0.0, 0.0, 0.0)
o = ORIGIN
id = IDLE
dk = DOCKED

setup = []

##---GENERAL GRAPHIC shape CLASS-------------------------------------------
class Peg(object):
    pass


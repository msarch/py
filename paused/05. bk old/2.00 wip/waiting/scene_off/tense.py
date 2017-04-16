#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * dec 2014 * bw-rev113
'''
from utils.toolkit import *

#--- SCENE --------------------------------------------------------------------
set_background_color(blue)

#--- SHAPES -------------------------------------------------------------------
'''
usage :
    name = Shape(kwargs, peg=Peg, vel=Vel)
    name=composite(k1,k2,k3,k4,k5,k6,k7,k8,s1,s2)
    show(name)
'''
gu = int(HEIGHT/100)  # grid unit size in pixel, used to size object relatively
V = HEIGHT  # a vert speed in pixel per second (here :1 screen-height/sec)
W = WIDTH

# h1=Baton(l=100,x1=( , ), x2=(,))
#--- DISPLAY LIST -------------------------------------------------------------
'''
usage :
    show(name,name2,...)
'''
#--- RULES --------------------------------------------------------------------
'''
ordrered ??? list of rules.
syntax : Rule(rule name, Actor(s)=target shape(s), named rule args=value)
'''

#------------------------------------------------------------------------------

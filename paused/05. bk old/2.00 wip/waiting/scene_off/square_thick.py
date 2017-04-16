#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * dec 2014 * bw-rev113
'''
from utils.toolkit import *
from random import choice

#--- SHAPES -------------------------------------------------------------------
'''
- shapes :
    name = SHAPE_TYPE(kwargs, peg=Peg, vel=Vel)
- shapes can be grouped :
    name = Shape( shapes=(k1,k2,k3,k4,k5,k6,k7,k8,s1,s2) peg=Peg, vel=Vel)
- shapes have position and velocity :
    peg = (x,y,z,angle)
    vel = (vx,vy, angular_velocity)
'''
gu = int(HEIGHT/85)  # grid unit size in pixel, used to size object relatively
V = HEIGHT  # base speed is one screen-height per second
W = WIDTH
w = 11 * gu
h = 33 * gu
origin = Blip()
# vertical rect
k1 = Rect(w=w, h=h, color=choice(kapla_colors), peg=Peg(-h/2, w/2, 0, 0))
# vertical rect
k3 = Rect(w=w, h=h, color=choice(kapla_colors), peg=Peg(h/2, -w/2, 0, 0))
# horizontal rect
k2 = Rect(w=h, h=w, color=choice(kapla_colors), peg=Peg(w/2, h/2, 0, 0))
# horizontal rect
k4 = Rect(w=h, h=w, color=choice(kapla_colors), peg=Peg(-w/2, -h/2, 0, 0))

#--- BIND TO CANVAS -----------------------------------------------------------
'''
- to display shapes add them to CANVAS :
    CANVAS.add(k1,k2,k3,k4)
'''
CANVAS.add(k1,k2,k3,k4,origin)

#--- RULES --------------------------------------------------------------------
'''
ordrered list of rules.                                                       # TODO
syntax : Rule(rule name, Actor(s)=target shape(s), named rule args=value)
'''
c=Cycle_Color(dummy,
        targets=(k1, k2, k3, k4),
        color_list=kapla_colors,
        ruletype='periodic',
        period=0.1
        )
#------------------------------------------------------------------------------

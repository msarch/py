#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# msarch@free.fr * jan 2015 * bw-rev113

from utils.toolkit import *
from random import choice

#--- SHAPES -------------------------------------------------------------------
'''
usage :
    name = Shape(kwargs, peg=Peg, vel=Vel)
    name=composite(k1,k2,k3,k4,k5,k6,k7,k8,s1,s2)
    show(name)
'''
gu = int(HEIGHT/85)  # grid unit size in pixel, used to size object relatively
V = HEIGHT  # base speed is one screen-height per second
W = WIDTH
e = 6 * gu
w = 11 * gu
h = 33 * gu
r = Rose()
bouncing_box=AABB(-W/2.0,-V/2.0,W/2.0,V/2.0)
bouncing_box2=AABB(-V/2.0,-V/2.0,V/2.0,V/2.0)

# four vertical rects
k1 = Rectangle_0(w=e, h=h, color=choice(kapla_colors), peg=Peg(w/2, w/2+e,0.99, 0))
k2 = Rectangle_0(w=e, h=h, color=choice(kapla_colors), peg=Peg(-w/2-e, w/2+e, 0.5, 0))
k3 = Rectangle_0(w=e, h=h, color=choice(kapla_colors), peg=Peg(w/2, -h-e-w/2, 0.5, 0))
k4 = Rectangle_0(w=e, h=h, color=choice(kapla_colors), peg=Peg(-w/2 - e, -h-e-w/2,1, 0))

# four horizontal rects
k5 = Rectangle_0(w=h, h=e, color=choice(kapla_colors), peg=Peg(w/2 + e, w/2, 1, 0))
k6 = Rectangle_0(w=h, h=e, color=choice(kapla_colors), peg=Peg(w/2 + e, -w/2-e, 1, 0))
k7 = Rectangle_0(w=h, h=e, color=choice(kapla_colors), peg=Peg(-h-e-w/2, w/2, 1, 0))
k8 = Rectangle_0(w=h, h=e, color=choice(kapla_colors), peg=Peg(-h-e-w/2, -w/2-e, 1, 0))

# horizontal slider
s1 = Rectangle_0(w=h, h=w, color=choice(kapla_colors), peg=Peg(-h/2, -w/2, 0, 0))
s1.vel=Vel(W,0,0)

# vertical slider
s2 = Rectangle_0(w=w, h=h, color=choice(kapla_colors), peg=Peg(-w/2, -h/2, 0.1, 0))
s2.vel=Vel(0,V,0)

#--- BIND TO CANVAS -----------------------------------------------------------
origin = (0,0,0)
scale = 1
speed = (0,0,0)
CANVAS.add(k1,k2,k3,k4,k5,k6,k7,k8,s1,s2)

#--- RULES --------------------------------------------------------------------
# ordrered list of rules.
# syntax : Rule(rule name, Actor(s)=target shape(s), named rule args=value)

sl=Slide(s1, s2)
bnc=Bounce(s1, box=bouncing_box)
bnc2=Bounce(s2, box=bouncing_box)
c=Cycle_Color(dummy,
        targets=(k1, k2, k3, k4),
        color_list=kapla_colors,
        ruletype='conditional',
        condition=('BUMP-X',s1)
        )
c2=Cycle_Color(dummy,  # Attention : 4 colors + 4 kapla = same recurent cycle
        targets=(k5, k6, k7, k8),
        color_list=kapla_colors,
        ruletype='conditional',
        condition=('BUMP-Y',s2)
        )
AGENTS.add(c1,c2)
#------------------------------------------------------------------------------

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * jan 2015 * bw-rev113
'''
from utils import *
from shapes import *
from agents import *

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
#origin = Blip()
#r = Rose()
bouncing_box=AABB(-W/2.0,-V/2.0,W/2.0,V/2.0)
bouncing_box2=AABB(-V/2.0,-V/2.0,V/2.0,V/2.0)
# four vertical rects
k1 = rectangle_0(w=e, h=h, color=choice(kapla_colors), peg=Peg(w/2, w/2+e,0.99, 0))
k2 = rectangle_0(w=e, h=h, color=choice(kapla_colors), peg=Peg(-w/2-e, w/2+e, 0.5, 0))
k3 = rectangle_0(w=e, h=h, color=choice(kapla_colors), peg=Peg(w/2, -h-e-w/2, 0.5, 0))
k4 = rectangle_0(w=e, h=h, color=choice(kapla_colors), peg=Peg(-w/2 - e, -h-e-w/2,1, 0))
# four horizontal rects
k5 = rectangle_0(w=h, h=e, color=choice(kapla_colors), peg=Peg(w/2 + e, w/2, 1, 0))
k6 = rectangle_0(w=h, h=e, color=choice(kapla_colors), peg=Peg(w/2 + e, -w/2-e, 1, 0))
k7 = rectangle_0(w=h, h=e, color=choice(kapla_colors), peg=Peg(-h-e-w/2, w/2, 1, 0))
k8 = rectangle_0(w=h, h=e, color=choice(kapla_colors), peg=Peg(-h-e-w/2, -w/2-e, 1, 0))
# horizontal slider
s1 = rectangle_0(w=h, h=w, color=choice(kapla_colors), peg=Peg(-h/2, -w/2, 0, 0))
# vertical slider
s2 = rectangle_0(w=w, h=h, color=choice(kapla_colors), peg=Peg(-w/2, -h/2, 0.1, 0))

s1.vel=Vel(W,0,0)
s2.vel=Vel(0,V,0)

#--- BIND TO CANVAS -----------------------------------------------------------
CANVAS.add(k1,k2,k3,k4,k5,k6,k7,k8,s1,s2)

#--- AGENTS --------------------------------------------------------------------
'''
ordrered list of agents.
syntax : Rule(agent name, Actor(s)=target shape(s), named agent args=value)
'''
sl=slide(s1, s2)
bnc=bounce(s1, box=bouncing_box)
bnc2=bounce(s2, box=bouncing_box)
c=cycle_color(dummy,
        targets=(k1, k2, k3, k4),
        color_list=kapla_colors,
        agenttype='conditional',
        condition=('BUMP-X',s1)
        )
c2=cycle_color(dummy,  # Attention : 4 colors + 4 kapla = same recurent cycle
        targets=(k5, k6, k7, k8),
        color_list=kapla_colors,
        agenttype='conditional',
        condition=('BUMP-Y',s2)
        )
#------------------------------------------------------------------------------

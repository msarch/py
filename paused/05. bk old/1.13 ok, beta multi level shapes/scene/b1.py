#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * dec 2014 * bw-rev113
'''
from utils.toolkit import *
from random import choice

#--- SCENE --------------------------------------------------------------------
set_background_color(blue)

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
origin = Blip()
r = Rose()
bouncing_box=AABB(-W/2.0,-V/2.0,W/2.0,V/2.0)
bouncing_box2=AABB(-V/2.0,-V/2.0,V/2.0,V/2.0)
# four vertical rects
k1 = Rect(w=e, h=h, color=choice(kapla_colors), peg=Peg(w/2, w/2+e,0.99, 0))
k2 = Rect(w=e, h=h, color=choice(kapla_colors), peg=Peg(-w/2-e, w/2+e, 0.5, 0))
k3 = Rect(w=e, h=h, color=choice(kapla_colors), peg=Peg(w/2, -h-e-w/2, 0.5, 0))
k4 = Rect(w=e, h=h, color=choice(kapla_colors), peg=Peg(-w/2 - e, -h-e-w/2,1, 0))
# four horizontal rects
k5 = Rect(w=h, h=e, color=choice(kapla_colors), peg=Peg(w/2 + e, w/2, 1, 0))
k6 = Rect(w=h, h=e, color=choice(kapla_colors), peg=Peg(w/2 + e, -w/2-e, 1, 0))
k7 = Rect(w=h, h=e, color=choice(kapla_colors), peg=Peg(-h-e-w/2, w/2, 1, 0))
k8 = Rect(w=h, h=e, color=choice(kapla_colors), peg=Peg(-h-e-w/2, -w/2-e, 1, 0))
# horizontal slider
s1 = Rect(w=h, h=w, color=choice(kapla_colors), peg=Peg(-h/2, -w/2, 0, 0))
# vertical slider
s2 = Rect(w=w, h=h, color=choice(kapla_colors), peg=Peg(-w/2, -h/2, 0.1, 0))

s1.vel=Vel(W/5,0,0)
s2.vel=Vel(0,V,0)

#--- BIND TO CANVAS -----------------------------------------------------------
CANVAS.add(k1,k2,k3,k4,k5,k6,k7,k8,s1,s2)

#--- RULES --------------------------------------------------------------------
'''
ordrered list of rules.
syntax : Rule(rule name, Actor(s)=target shape(s), named rule args=value)
'''
sl=Slide(s1, s2)
bnc=Bounce(s1, box=bouncing_box)
bnc2=Bounce(s2, box=bouncing_box2)
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
#------------------------------------------------------------------------------

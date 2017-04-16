#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev109
'''
from shapes import Rect, Blip, Compound, Rose, show
from rules import Slide, Bounce, Cycle_Color
from utils.cfg import background_color, black, white, blue, red, blue50, \
        kapla_colors, Peg, Vel, SCREEN, HEIGHT

#--- SCENE --------------------------------------------------------------------
background_color(white)

#--- PATHS / PEGS ------------------------------------------------------------- TODO
#Peg(p2, (50,50)) # check if Peg concept is necessary. Replace w Point?
#Axis
#Grid

#--- SHAPES -------------------------------------------------------------------
gu = int(HEIGHT/85)  # grid unit size in pixel, used to size object relatively
V = HEIGHT  # base speed is one screen-height per second
e = 6 * gu
w = 11 * gu
h = 33 * gu
origin = Blip()
r = Rose()

k1 = Rect(w=e, h=h, color=red, peg=Peg(w/2, w/2+e, 0))
k2 = Rect(w=e, h=h, color=blue50, peg=Peg(-w/2-e, w/2+e, 0))
k3 = Rect(w=e, h=h, color=blue, peg=Peg(w/2, -h-e-w/2, 0))
k4 = Rect(w=e, h=h, color=black, peg=Peg(-w/2 - e, -h-e-w/2, 0))

k5 = Rect(w=h, h=e, color=blue, peg=Peg(w/2 + e, w/2, 0))
k6 = Rect(w=h, h=e, color=blue, peg=Peg(w/2 + e, -w/2-e, 0))
k7 = Rect(w=h, h=e, color=blue, peg=Peg(-h-e-w/2, w/2, 0))
k8 = Rect(w=h, h=e, color=blue, peg=Peg(-h-e-w/2, -w/2-e, 0))

s1 = Rect(w=h, h=w, color=blue, peg=Peg(-h/2, -w/2, 0))
s2 = Rect(w=w, h=h, color=blue, peg=Peg(-w/2, -h/2, 0))

star=Compound(k1,k2,k3,k4,k5,k6,k7,k8,s1,s2)
mickey=Compound(k1,k2,k3,k4,k5,k6,k7,k8, peg=Peg(100,-100,45))

show(mickey,star)
#--- COLLECT ------------------------------------------------------------------
'''
shapes are added to GROUPS i.e. an ordered? list of stuff
and any attributes can be added to groups as well as shapes
'''
#s1.vel=Vel(V,0,0)
#s2.vel=Vel(0,V,0)
#Actor('c2', cshapes='pac', peg=dk)  # possibly give either 2 or 3 coord or peg TODO


#--- RULES --------------------------------------------------------------------
'''
ordrered list of rules.
syntax : Rule(rule name, Actor(s)=target shape(s), named rule args=value)
'''
#Visible = [b1,k1,k2,k3,k4,k5,k6,k7,k8,s1,s2,mickey]
#Slide.register(s1, s2,)
#Bounce.register(s1, s2, rect=SCREEN)  # add broadcast = True                   TODO
#Cycle_Color(s1, s2, color_list=kapla_colors, period=2)

# voir décorateurs pour conditional rules et broadcast rules                    TODO

#------------------------------------------------------------------------------

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev109
'''
from shapes import Rect, Blip
from actors import Actor
from rules import  Slide, Bounce, Cycle_Color
from utils.cfg import background_color, black, blue, kapla_colors,\
        Vel, SCREEN, HEIGHT

#--- SCENE --------------------------------------------------------------------
background_color(black)

#--- PATHS / PEGS ------------------------------------------------------------- TODO
#Peg(p2, (50,50)) # check if Peg concept is necessary. Replace w Point?
#Axis
#Grid

#--- SHAPES -------------------------------------------------------------------
g=int(HEIGHT/85)  # grid Actor size, used to size object relatively
V=HEIGHT  # base speed is one screen-height per second
e=6*g
w=11*g
h=33*g
Blip('b1')

Rect('k1', w=e, h=h, color=blue).offseted(w/2, w/2+e)
Rect('k2', w=e, h=h, color=blue).offseted(-w/2-e, w/2+e)
Rect('k3', w=e, h=h, color=blue).offseted(w/2, -h-e-w/2)
Rect('k4', w=e, h=h, color=blue).offseted(-w/2 -e, -h-e-w/2)

Rect('k5', w=h, h=e, color=blue).offseted(w/2 + e, w/2)
Rect('k6', w=h, h=e, color=blue).offseted(w/2 + e, -w/2-e)
Rect('k7', w=h, h=e, color=blue).offseted(-h-e-w/2, w/2)
Rect('k8', w=h, h=e, color=blue).offseted(-h-e-w/2, -w/2-e)

Rect('s1', w=h, h=w, color=blue).offseted(-h/2, -w/2)
Rect('s2', w=w, h=h, color=blue).offseted(-w/2, -h/2)

#--- ActorS --------------------------------------------------------------------
'''
shapes are added to the scene via an ordered list of Actors
and displayed FIFO
'''
Actor('b1', shape='b1')

Actor('k1', shape='k1')
Actor('k2', shape='k2')
Actor('k3', shape='k3')
Actor('k4', shape='k4')
Actor('k5', shape='k5')
Actor('k6', shape='k6')
Actor('k7', shape='k7')
Actor('k8', shape='k8')


Actor('s1', shape='s1', vel=Vel(V,0,0))
Actor('s2', shape='s2', vel=Vel(0,V,0))
#Actor('c2', cshapes='pac', peg=dk)  # possibly give either 2 or 3 coord or peg TODO

#--- RULES --------------------------------------------------------------------
'''
ordrered list of rules.
syntax : Rule(rule name, Actor(s)=target shape(s), named rule args=value)
'''
Slide('slide_h', actors=('s2',))
Slide('slide_v', actors=('s1',))
Bounce('screen_bounce', actors=('s1', 's2'), rect=SCREEN)  # broadcast = True   TODO
Cycle_Color('cycle', actors=('s1', 's2'), color_list=kapla_colors, period=2)

# voir décorateurs pour conditional rules et broadcast rules

#------------------------------------------------------------------------------


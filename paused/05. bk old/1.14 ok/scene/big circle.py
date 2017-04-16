#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * nov 2014 * bw-rev112
'''
from utils import *
from shapes import *
from agents import *


#--- SCENE --------------------------------------------------------------------
#--- SHAPES -------------------------------------------------------------------
'''
usage :
    name = Shape(kwargs, peg=Peg, vel=Vel)
    name=composite(k1,k2,k3,k4,k5,k6,k7,k8,s1,s2)
    show(name)
'''
#H = HEIGHT  # base per second vert speed is one screen-height
#W = WIDTH  # base per second vert speed is one screen-height

#gu = int(HEIGHT/85)  # grid unit size in pixel, used to size object relatively
#VY = H*1.0  # one screen-height per second
#VX = W*0.2  # 5 sec for one screen-width

#e = 6 * gu
#w = 11 * gu
#h = 33 * gu

#origin = Blip()
#r = Rose()
#bouncing_box=AABB(-W/2.0,-H/2.0,W/2.0,H/2.0)
#radius = H/2
## big circle
#c=very_light_grey
#cc1=Disk(x=0,y=0,radius=radius, color= c ,peg=Peg(0, 0, -0.9, 0))
#cc1.vel=Vel(VX/5,0,0)


##--- BIND TO CANVAS -----------------------------------------------------------
#CANVAS.add(cc1)

##--- AGENTS --------------------------------------------------------------------
#'''
#ordrered list of agents.
#syntax : Rule(agent name, Actor(s)=target shape(s), named agent args=value)
#'''
#sl=Slide(cc1)
#bnc=Bounce(cc1, box=bouncing_box)
##------------------------------------------------------------------------------

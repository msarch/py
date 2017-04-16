#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * nov 2014 * bw-rev112
'''
from utils import *
from shapes import *

H = HEIGHT  # base per second vert speed is one screen-height
W = WIDTH  # base per second vert speed is one screen-height
radius = H/2

#--- SHAPES -------------------------------------------------------------------
# big circle
c=very_light_grey
cc1=Disk(x=0,y=0,radius=radius, color= c ,peg=Peg(0, 0, -0.9, 0))
cc1.vel=Vel(VX/5,0,0)

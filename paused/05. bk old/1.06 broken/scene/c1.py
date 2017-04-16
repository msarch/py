#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev106
'''
from shapes import Rect, Blip, Kapla
from cells import Cell, lmnts
from utils.cfg import background_color, blue, orange, red


#--- PATHS / PEGS ------------------------------------------------------------- TODO

#--- SCENE --------------------------------------------------------------------
background_color(orange)
#Peg(p2, (50,50)) # check if Peg concept is necessary. Replace w Point?
#Axis
#Grid

#--- SHAPES -------------------------------------------------------------------
Blip('b1')
Kapla('k1', color=blue).offset(100,200)
Rect('r1', color=(0,1,1,1), w=100, h=300) # or just p2 if p1 = 0
Rect('hslider', color=red, w=100, h=300) # or just p2 if p1 = 0
# CShape(pac, Pacman)
# Shape(line (p1,p2)) # pr just p2 if p1 = 0                                    TODO
#s = Ghost(Color.blue).offset(0,0)                                              TODO

#--- CELLS --------------------------------------------------------------------
# shapes are added to the scene via an ordered list of Cells
# and thus displayed FIFO
Cell('c1', shape='b1')
Cell('c2', shape='b1')
print ''
print 'cells.lmnts viewed from c1', lmnts
#Cell(c2, cshapes='pac', peg=dk)  # possibly give either 2 or 3 coord or peg    TODO

#--- RULES --------------------------------------------------------------------
# ordrered list of rules.
# syntax : Rule(cell(s)=target shape(s), named rule args=value)
#Step('c1', dx=200, dy=20)
#Spin('c1', av=10)
#Bounce('hslider',rect=SCREEN)
#r4=Toggle(kwd=r3.bounced, toggle=r2.change_av)
#r5=
#randomize_color((Kapla_colors,10),[k])


#-----------------------------------------------------------------------------


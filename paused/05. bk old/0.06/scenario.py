#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : setup and mod shapes

# r0.1

##--- SPECIFIC DRAWING HERE ------------------------------------------------------------------------

import toxy
from greom import Point, SimpleLine, SimpleRec, ObGeom
from toxy import *

##--- SPECIFIC DRAWING HERE ------------------------------------------------------------------------

debug=1
drawing_list=[]

##--- SPECIFIC DRAWING HERE ------------------------------------------------------------------------

def geom_draw():
    for lmnt in drawing_list:
        lmnt.pygDraw()      # --- PYGLET OUTPUT
        if debug :
            print(lmnt)     # --- TEXT OUTPUT
        #obgeom.pdfy()      # --- PDF OUTPUT
        #obgeom.dxfy()      # --- DXF OUTPUT
        #obgeom.rhinofy()   # --- RHINO OUTPUT
        #obgeom.imagify()   # --- IMAGE OUTPUT
        

        
##--- SPECIFIC DRAWING HERE ------------------------------------------------------------------------

def geom_init():
    a = Point(10,100)
    line1 = SimpleLine(10,10,10,180)   # startpoint, endpoint
    rec1 = SimpleRec(10,180,20,300)    # basepoint, width, height
    rec2 = rec1.copy()
     
    drawing_list.append(a)
    drawing_list.append(line1)
    drawing_list.append(rec1)
    drawing_list.append(rec2)
    
##--- SPECIFIC DRAWING HERE ------------------------------------------------------------------------

def geom_update(dt):
	m=toxy.tm(1,0)
	for lmnt in drawing_list:
		lmnt.operate(m)

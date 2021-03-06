#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
scene bw engine :: rev_103 :: 2014_JUNE :: msarch@free.fr
'''
#--- IMPORTS ------------------------------------------------------------------
from bw import *

#--- SHAPES -------------------------------------------------------------------
s = Shape([Ghost(Color.blue).offset(100, 100)])
r = Shape([Rect(400,400, Color.red)])

#--- CELLS --------------------------------------------------------------------
g = Cell(shape=s, posx=100, posy=100, vx=150.0, vy=50.0, va=0.0)
h = Cell(shape=r, posx=400, posy=400)

#--- RULES --------------------------------------------------------------------
r1 = Move()
r2 = Bounce(0,0,1280,800)

#--- BIND ---------------------------------------------------------------------
bind(r2,g)
bind(r1,g)

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    set_background(Color.orange)
    animate()
    #export(duration=3.5)



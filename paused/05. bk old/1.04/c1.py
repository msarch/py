#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * july 2014 * bw-rev104
'''
#--- IMPORTS ------------------------------------------------------------------
from bw import *


#--- SHAPES -------------------------------------------------------------------
k = Kapla(Color.black)
s = Shape([Ghost(Color.blue).offset(0,0)])
r = Shape([k, Rect(100,100, Color.red), k.offset(100,0)])

#--- CELLS --------------------------------------------------------------------

#display = [
        #0, background, Color.orange,
        #1, s, (0,100),
        #2, r,(100,200),
        #3, r,(400,400)
        #]
#rules = [
        #s,(10,10,0)
        #]


g = Cell(shape=s, posx=0, posy=0, vx=0.0, vy=0.0, va=1.0)
h = Cell(shape=r, posx=0, posy=0)

#--- RULES --------------------------------------------------------------------
r1 = Move(10,10)
r2 = Bounce(0,0,1280,800)

#--- BIND ---------------------------------------------------------------------
r2.bind(g)
r1.bind(g)

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    set_background(Color.orange)
    animate()
    #export(duration=3.5)



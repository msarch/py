#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
scene bw engine :: rev_102 :: 2014_JUNE :: msarch@free.fr
'''

##  IMPORTS -------------------------------------------------------------------
from bw import *

#- ACTORS ---------------------------------------------------------------------

# TODO : where is DATA stored ???
        # i.e. : number of actors, gradient or forces field...
        # here acces to other actors publications, position
s = Shape([Ghost(Color.black).offset(10, 10)],
        posx=100, posy =100,
        vx=150.0,vy=50.0,
        va=0.0)
g = Cell(shape=s)


#black_ghost = Primitive(ghost_contour, Color.black).offset(+200, +105)
#orange_ghost = Primitive(ghost_contour, Color.orange).offset(+300, +200)
#kapla= Rect(10, 100, 120, 200, Color.white).offset(100, 200)
#s = Shape([orange_ghost, black_ghost,kapla])

# TODO
#- RULES ----------------------------------------------------------------------
r1 = Move()
r2 = Bounce(0,0,1280,800)

Field.bind(r2,g)
Field.bind(r1,g)
Field.color = Color.orange

##-----------------------------------------------------------------------------
if __name__ == "__main__":
    ''' init of a new pyglet window setup, and run
    '''
    animate()
    #export(duration=3.5)



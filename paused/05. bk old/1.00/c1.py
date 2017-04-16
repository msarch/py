#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
scene for zululand engine :: rev_24 :: MAY2014 :: msarch@free.fr
'''

##  IMPORTS -------------------------------------------------------------------
from bw.field import Field, Cell
from bw.rules import Move, Bounce
from bw.shapes import Shape, Ghost, Color
from bw.animate import animate, export

#-ACTOR SUBCLASS---------------------------------------------------------------

f = Field()

# TODO : where is DATA stored ???
        # i.e. : number of actors, gradient or forces field...
        # here acces to other actors publications, position
s = Shape([Ghost(Color.black).offset(100, 200)])
g = Cell(shape=s,vx=150,vy=50,va=0)


#black_ghost = Primitive(ghost_contour, Color.black).offset(+200, +105)
#orange_ghost = Primitive(ghost_contour, Color.orange).offset(+300, +200)
#kapla= Rect(10, 100, 120, 200, Color.white).offset(100, 200)
#s = Shape([orange_ghost, black_ghost,kapla])



r1 = Move()
r1.add(g)
r2 = Bounce(0,0,1280,800)
r2.add(g)
f.display(g)
f.eval(r1)  #resoudrait le pb d'init de rules un genre de scenario
f.eval(r2)

##-----------------------------------------------------------------------------
if __name__ == "__main__":
    ''' init of a new pyglet window setup, and run
    '''
    #animate(f)
    export(f,duration=3.5)



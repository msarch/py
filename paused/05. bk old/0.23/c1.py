#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/scene/creature1 :: rev_23 :: MAY2014 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from bw.field import Field, Cell, Move
from bw.shapes import Shape, Ghost, Color
from bw.animate import animate

#-ACTOR SUBCLASS---------------------------------------------------------------

f = Field()

# TODO : where is DATA stored ???
        # i.e. : number of actors, gradient or forces field...
        # here acces to other actors publications, position
s = Shape([Ghost(Color.black)])
g = Cell(shape=s)


#black_ghost = Primitive(ghost_contour, Color.black).offset(+200, +105)
#orange_ghost = Primitive(ghost_contour, Color.orange).offset(+300, +200)
#kapla= Rect(10, 100, 120, 200, Color.white).offset(100, 200)
#s = Shape([orange_ghost, black_ghost,kapla])



r1 = Move(a=0,dx=5,dy=5)
r1.add(g)

f.display(g)
f.eval(r1)  #resoudrait le pb d'init de rules un genre de scenario


##-----------------------------------------------------------------------------
if __name__ == "__main__":
    ''' init of a new pyglet window setup, and run
    '''
    animate(f)



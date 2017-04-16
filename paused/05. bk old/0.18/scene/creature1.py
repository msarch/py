#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: actors :: rev 16 :: 02.2014 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from shapes import Shape, Primitive, Rect, Color
from scene import Actor


#-ACTOR SUBCLASS---------------------------------------------------------------
def tick(actor,dt):
    print 'tick Ghost'
    actor.angle +=1


#-actual actor definition------------------------------------------------------

def register():
    ghost = [
        (-7, -7),   # 0
        (-7.0, 0.0),# 1
        (-5, -5),   # 22
        (-6.7, 2.0),# 2
        (-3, -7),   # 21
        (-5.9, 3.8),# 3
        (-1, -7),   # 20
        (-4.6, 5.3),# 4
        (-1, -5),   # 19
        (-2.9, 6.4),# 5
        (1, -5),    # 18
        (-1.0, 6.9),# 6
        (3, -7),    # 16
        (1.0, 6.9), # 7
        (5, -5),    # 15
        (2.9, 6.4), # 8
        (7, -7),    # 14
        (4.6, 5.3), # 9
        (7.0, 0.0), # 13
        (4.6, 5.3), # 10
        (6.7, 2.0), # 12
        (5.9, 3.8), # 11
        ]

    s = Shape([
        Primitive(ghost, Color.black).offset(+200, +105),
        Primitive(ghost, Color.orange).offset(+300, +200),
        Rect(100, 100, 120, 200, Color.red).offset(100, 200),
        Rect(100, 100, 120, 200, Color.red).rotate(10).offset(200, 600)
        ])

    g = Actor()
    g.shape = s
    g.tick = tick
    return(g)

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/scene/shapes :: rev 21 :: MAY2014 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from geometry import Shape, Primitive, Color, Rect


ghost_contour = [
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


black_ghost = Primitive(ghost_contour, Color.black).offset(+200, +105)
orange_ghost = Primitive(ghost_contour, Color.orange).offset(+300, +200)
kapla= Rect(10, 100, 120, 200, Color.white).offset(100, 200)

s = Shape([orange_ghost, black_ghost,kapla])

s2 = Shape([orange_ghost, black_ghost,kapla, \
         Rect(10, 100, 120, 200, Color.red).rotate(10).offset(200, 600)])



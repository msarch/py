#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# TT : General geometry lib 2d

from math import degrees, atan2
from math import sqrt, pow
from math import radians, sin, cos

def angle(x0, y0, x1, y1):
    return degrees( atan2(y1-y0, x1-x0) )

def distance(x0, y0, x1, y1):
    return sqrt(pow(x1-x0, 2) + pow(y1-y0, 2))

def coordinates(x0, y0, distance, angle):
    x1 = x0 + cos(radians(angle)) * distance
    y1 = y0 + sin(radians(angle)) * distance
    return x1, y1

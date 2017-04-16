#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 13-d2 :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
import random

from pygland import Land
from rules import Slide
from shapes import Rect
from zulus import Zulu

##  CONSTANTS AND VARIABLES ---------------------------------------------------

#--- FUNCTIONS ----------------------------------------------------------------
def populate():
    # define zulus
    for i in range (1,160):
        x=random.uniform(1,1280)
        y=random.uniform(1,800)
        shp=Rect(2,2)
        pos=[x,y,0.0]
        a=0 # angle
        r=random.uniform(0,1.0)
        g=random.uniform(0,1.0)
        b=random.uniform(0,1.0)
        a=random.uniform(0,1.0)
        col=[r,g,b,a]
        z= Zulu(shp,pos,a,col)

    #Define as many rules as necessary
        r1=Slide((random.uniform(-120,120),random.uniform(-80,80)))

    # append zulus to rules
        r1.add(z)
    for i in range (1,160):
        x=random.uniform(1,1200)
        y=random.uniform(1,800)
        shp=Rect(20,20)
        pos=[x,y,0.0]
        a=0 # angle
        r=random.uniform(0,1.0)
        g=random.uniform(0,1.0)
        b=random.uniform(0,1.0)
        a=random.uniform(0,1.0)
        col=[r,g,b,a]
        z= Zulu(shp,pos,a,col)

    # ruleset.sort # <-- FIXME later

##  MAIN ----------------------------------------------------------------------
def main():
    L=Land()
    populate()
    L.run()
    #pyglet loop will manage display and updates

##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()


# TODO : implement shaders (from nodebox graphics
# TODO : implement groups or layers
# TODO : shapes have an anchor
#        to which displacements are applied
# TODO : objects can be cooked after transformation
# TODO : subpixel movement
# DONE : use camera module from 'manytriangles'
# TODO : use colors module

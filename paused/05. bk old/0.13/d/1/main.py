#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 13-d :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from zululand import Zulu,Land
from rules import Slide
from shapes import Rect
import random
import pygtools

##  CONSTANTS AND VARIABLES ---------------------------------------------------
FPS=60
BGCOLOR=(0.0,120.0,0.0,0.0)
LANDSIZE=pygtools.get_display_size()

#--- FUNCTIONS ----------------------------------------------------------------
def populate():
    # define zulus
    for i in range (1,2000):
        x=random.uniform(1,1280)
        y=random.uniform(1,800)
        shp=Rect(20,20)
        pos=[x,y,0.0]
        r=random.uniform(0,1.0)
        g=random.uniform(0,1.0)
        b=random.uniform(0,1.0)
        a=random.uniform(0,1.0)
        col=[r,g,b,a]
        z= Zulu(shp,pos,col)

    #Define as many rules as necessary
        vx=random.uniform(-120,120)
        vy=random.uniform(-80,80)
        r1=Slide(vx,vy)

    # append zulus to rules
        r1.add(z)
    for i in range (1,100):
        x=random.uniform(1,1200)
        y=random.uniform(1,800)
        shp=Rect(20,20)
        pos=[x,y,0.0]
        r=random.uniform(0,1.0)
        g=random.uniform(0,1.0)
        b=random.uniform(0,1.0)
        a=random.uniform(0,1.0)
        col=[r,g,b,a]
        z= Zulu(shp,pos,col)

    # ruleset.sort # <-- FIXME later

##  MAIN ----------------------------------------------------------------------
def main():
    print LANDSIZE
    ZL=Land(LANDSIZE,FPS,BGCOLOR)
    populate()
    ZL.run()
    #pyglet loop will manage display and updates

##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()


# TODO : implement shaders (from nodebox graphics
# TODO : implement groups or layers
# TODO : shapes have an origin/centroid/reference point/handle
#        to which displacements are applied
# TODO : objects can be cooked after transformation


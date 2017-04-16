#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 13-c :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
import pyglet
import zululand
import display
from zululand import Zulu
from rules import Slide
from shapes import Rect
import random

#--- FUNCTIONS ----------------------------------------------------------------
def populate():
    # define zulus

    for i in range (1,2000):
        print i
        z= Zulu()
        x=random.randint(1,1200)
        y=random.randint(1,800)

        z.shape=Rect(20,20)
        z.position=[x,y]

        vx=random.randint(-120,120)
        vy=random.randint(-80,80)

    #Define as many rules as necessary
        r1=Slide(vx,vy)
    # append zulus to rules
        r1.add(z)

    # ruleset.sort # <-- FIXME later

##  MAIN ----------------------------------------------------------------------
def main():
    land_size=display.get_size()
    background_color=(0.0,0.0,0.0,0.0)
    TheLand=zululand.Land(land_size,background_color)
    TheDisplay=display.Window(TheLand)
    populate()
    #pyglet loop will manage display and updates
    pyglet.app.run()

##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()

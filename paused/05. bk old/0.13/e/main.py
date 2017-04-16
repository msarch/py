#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 13-e :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
import random
from engine import Engine
from rules import Slide
from shapes import Shape, Rect, Color
from zulus import Zulu, Body

##  CONSTANTS AND VARIABLES ---------------------------------------------------
global DEBUG, END_TIME, PREVIEW_SIZE, BGGCOLOR, FPS, PicPS

DEBUG=1
END_TIME = 3 # EXPORT MODE : duration (seconds) of the anim
PREVIEW_SIZE =(800,600)
BGCOLOR =Color.very_light_grey # background
FPS= 60 # display max framerate
PicPS = 25  # EXPORT MODE FRAMERATE : images per second for movie export

##  --- FUNCTIONS -------------------------------------------------------------
def definitions():
#    # define zulus
    #for i in range (1,160):
        #x=random.uniform(1,1280)
        #y=random.uniform(1,800)
        #body=Rect(20,20)
        #anchor=[x,y,0.0]
        #angle=0 # angle
        #r=random.uniform(0,1.0)
        #g=random.uniform(0,1.0)
        #b=random.uniform(0,1.0)
        #a=random.uniform(0,1.0)
        #color=[r,g,b,a]
        #z= Zulu(body,anchor,angle,color)

    ##Define as many rules as necessary
        #r1=Slide((random.uniform(-120,120),random.uniform(-80,80)))

    ## append zulus to rules
        #r1.add(z)
    #for i in range (1,160):
        #x=random.uniform(1,1200)
        #y=random.uniform(1,800)
        #shp=Rect(20,20)
        #pos=[x,y,0.0]
        #a=0 # angle
        #r=random.uniform(0,1.0)
        #g=random.uniform(0,1.0)
        #b=random.uniform(0,1.0)
        #a=random.uniform(0,1.0)
        #col=[r,g,b,a]
        #z= Zulu(shp,pos,a,col)


    egg_white = [
        -10, -25,
        -20, -15,
        +10, -25,
        -20, +15,
        +20, -15,
        -10, +25,
        +20, +15,
        +10, +25,
    ]
    egg_yellow = [
        -10, -10,
        -10, +10,
        +10, -10,
        +10, +10,
    ]
    b = Body([
        Shape(egg_white, Color.white).offset(+200, +105),
        Shape(egg_yellow, Color.orange).offset(+300, +200),
        Rect(100,100,120,200, Color.red).offset(100,200),
        Rect(100,100,120,200, Color.red).rotate(10).offset(200,600)
    ])
    toto= Zulu(body=b)
    rule1=Slide((random.uniform(-12,12),random.uniform(-8,8)))
    engine.ruleset.add(rule1,toto)




   # ruleset.sort # <-- FIXME later

##  MAIN ----------------------------------------------------------------------
def main():
    engine=Engine(MODE='PREVIEW') # options are : 'FULL'; 'PREVIEW'; 'EXPORT'
    definitions()
    engine.run()

##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()



#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 13-d3 :: 10.2013 :: msarch@free.fr

##  TO DO LIST ----------------------------------------------------------------
# TODO : BAKE
# objects can be 'baked' after transformation
# and maybe moved to a still group (no glmove) for optimization
# TODO : OPTIMISATION:
# staticmethod optim
# render with functions inlieu of classes methods?
# TODO : SHADERS
# implement shaders (from nodebox graphics
# TODO : SPLINES & OTHER bodyS
# use path for splines and oher bodys. Unify draw mode(shoebot/ nodebox /
# TODO :SUBPIXEL
# subpixel movement?

##  TO DO SORTED ----------------------------------------------------------------
# 1 focus on input, animation and render(png,pdf, openGL) with RECTS only
# 2 zulus have points :
# 3 app structure : ZULU CLASS, ANCHORS, BAKE, COLOR STROKE & FILL
# 4 performance and render issues : VERTEX LISTS, 25 IMAGES/S, EXPORT
# 99 later : SHADERS, SUBPIXEL, SPLINES & OTHER bodyS

##  REMOVED -------------------------------------------------------------------
# CAMERA : useless, complicated, camera mvt not needed yet

##  IMPORTS -------------------------------------------------------------------
import random
from engine import Engine
from rules import Slide
from shapes import Primitive as Prim, Body, Rect, Color
from zulus import Zulu

##  CONSTANTS AND VARIABLES ---------------------------------------------------
engine=Engine(MODE='PREVIEW') # options are : 'FULL'; 'PREVIEW'; 'EXPORT'

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
    sh = Body([
        Prim(egg_white, Color.white).offset(+200, +105),
        Prim(egg_yellow, Color.orange).offset(+300, +200),
        Rect(100,100,120,200, Color.red).offset(100,200),
        Rect(100,100,120,200, Color.red).rotate(10).offset(200,600)
    ])
    toto= Zulu(body=sh)
    rule1=Slide((random.uniform(-12,12),random.uniform(-8,8)))
    engine.ruleset.add(rule1,toto)




   # ruleset.sort # <-- FIXME later

##  MAIN ----------------------------------------------------------------------
def main():
    definitions()
    engine.run()

##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()



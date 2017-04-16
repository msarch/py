#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : scene setup main module

# r0.8

##  IMPORTS -----------------------------------------------------------------

from pygloop import Canvas  # main pyglet loop
from pyglet import clock
from grobs import *         # 2d graphic objects primitives
                            # available geometry from grobs :
                            #    Point()
                            #    Line()
                            #    Rect()
from flatmath import *      # 2d geometry operations toolbox
                            # available matrix from flatmath
                            #    im = identity()
                            #    tm = translation()
                            #    sm = scale()
                            #    rm = rotation()
                            #    xsm = x_symetry()
                            #    ysm = y_symetry()
                            #    gsm = general_symetry()
                            #    mmult(m,M) = matrix multiplication 
from random import randint

##  CONSTANTS AND VARIABLES ---------------------------------------------------
fps=25.0                    # windows refresh rate
canvas=Canvas(fps)          # standard fullscreen window

actors1=[]
tintors1=[]
tintors2=[]
tintors3=[]

##  DRAWING BEGINS HERE -------------------------------------------------------
def scene_setup():
    
    g=8 # grid cell size
    Grid(g,canvas.width,canvas.height)   # square grid, origin @ screen center
    Scope(canvas.width,canvas.height)    # scope, origin @ screen center

# GROBS LIST -------------------------------------------------------

# TODO : taille des rectangles fonction de la taille écran

    e,w,h =6*g,11*g,33*g
    clr = (0.5,0.6,0.1)
    r1 = Rect(h, e,-w/2-h/2-e,e/2+w/2,clr) # basepoint, width, height
    r2 = r1.copy()
    r2.m_transform(xsm())
    r3 = r1.copy()
    r3.m_transform(ysm())
    r4 = r3.copy()
    r4.m_transform(xsm())
    r5 = Rect(e,h,-w/2-e/2,w/2+e+h/2,clr)
    r6 = r5.copy()
    r6.m_transform(ysm())
    r7 = r5.copy()
    r7.m_transform(xsm())
    r8 = r7.copy()
    r8.m_transform(ysm())
    
    m=tm(4,0)
    r9 = Rect(h,w,0,0,clr,m)

    m = tm(1,1)
    a = Point(0,0,clr,m)

# ACTORS LIST  ----------------------------------------------------------------
    # regular elements of the canvas will bypass the update method
    # 'actors' list will be update by 'actors_update()' every dt
    actors1.extend([r9]) # use extend to add multiple elements
    clock.schedule_interval(actors1_update, 1.0/25)
    #actors.append(line1) # use append to add a single element

# TINTORS LIST  ---------------------------------------------------------------
    tintors1.extend([r9,r8,r5])
    tintors2.extend([r1,r4,r6])
    tintors3.extend([r2,r3,r7])
    clock.schedule_interval(tintors1_update, 1.20)
    clock.schedule_interval(tintors2_update, 1.0)
    clock.schedule_interval(tintors3_update, 0.3)

def actors1_update(dt): #dt is defined in
    global actors1
    for grob in actors1 : grob.transform()

def tintors1_update(dt): #dt is defined in
    global tintors1
    for grob in tintors1 : grob.color = (randint(5,255)/255.0,\
                                       randint(5,255)/255.0,\
                                       randint(5,255)/255.0)

def tintors2_update(dt): #dt is defined in
    global tintors2
    for grob in tintors2 : grob.color = (randint(5,255)/255.0,\
                                       randint(5,255)/255.0,\
                                       randint(5,255)/255.0)

def tintors3_update(dt): #dt is defined in
    global tintors3
    for grob in tintors3 : grob.color = (randint(5,255)/255.0,\
                                       randint(5,255)/255.0,\
                                       randint(5,255)/255.0)


##  MAIN ----------------------------------------------------------------------

def main():
    scene_setup()
    canvas.run()

##  ------------------------------------------------------------------------------

if __name__ == "__main__": main()

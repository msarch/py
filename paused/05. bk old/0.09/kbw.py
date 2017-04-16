#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : scene setup main module

# kbw r0.9

##  IMPORTS -------------------------------------------------------------------

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
from random import choice
from htmlpalette import kapla_colors

##  CONSTANTS AND VARIABLES ---------------------------------------------------
fps = 25.0                  # windows refresh rate
c = Canvas(fps)        # standard fullscreen window
g=int(c.screen_height/85)  # grid cell size.
                                # can be used to size object relatively
cw,ch =c.width,c.height
cl,cr,ct,cb=-cw*0.5,cw*0.5,ch*0.5,-ch*0.5
#Grid(g,cw,ch)   # square grid, origin @ screen center
#Scope(cw,ch)    # scope, origin @ screen center
actors1=[]
actors2=[]
tintors1=[]
tintors2=[]
tintors3=[]
hfac=-2.0
vfac=-1.5
##  DRAWING BEGINS HERE -------------------------------------------------------
def scene_setup():
# GROBS LIST ------------------------------------------------------------------
    e=6*g
    w=11*g
    h=33*g

    r1 = Rect(h, e,-w/2-h/2-e,e/2+w/2,(choice(kapla_colors)))
    r2 = r1.copy()
    r2.once_transform(xsm())
    r3 = r1.copy()
    r3.once_transform(ysm())
    r4 = r3.copy()
    r4.once_transform(xsm())
    r5 = Rect(e,h,-w/2-e/2,w/2+e+h/2,(choice(kapla_colors)))
    r6 = r5.copy()
    r6.once_transform(ysm())
    r7 = r5.copy()
    r7.once_transform(xsm())
    r8 = r7.copy()
    r8.once_transform(ysm())

    m=tm(7,0)
    h_slider = Rect(h,w,0,0,(choice(kapla_colors)),m)

    m=tm(0,5)
    v_slider = Rect(w,h,0,0,(choice(kapla_colors)),m)

    m = tm(1,1)
    a = Point(0,0,(choice(kapla_colors)),m)

# SCHEDULED ACTIONS LIST ------------------------------------------------------

    actors1.extend([h_slider]) #.extend: add multiple elements,.append: add one
    clock.schedule_interval(actors1_update, 1/fps)

    actors2.extend([v_slider]) #.extend: add multiple elements,.append: add one
    clock.schedule_interval(actors2_update, 1/fps)

    tintors1.extend([a,r8,r5])
    tintors2.extend([r1,r4,r6])
    tintors3.extend([r2,r3,r7])

def actors1_update(dt): #dt is defined in
    global actors1,hfac
    for a in actors1 :
        a.transform()
        if (a.v[1][0]<cl or a.v[2][0]>cr):  # if bounce,
           # a.M[2] *=-1                         # reverse dir
            a.color = choice(kapla_colors)      # change clr
            a.M[2] *= hfac                         # change speed
            hfac=1.0/hfac
            tintors1_update()


def actors2_update(dt): #dt is defined in
    global actors2,vfac
    for a in actors2 :
        a.transform()
        if (a.v[4][1]>ct or a.v[1][1]<cb):  # if bounce,
            #a.M[5] *=-1                         # reverse dir
            a.color = choice(kapla_colors)      # change clr
            a.M[5] *= vfac                         # change speed
            vfac=1.0/vfac
            tintors2_update()
            tintors3_update()

def tintors1_update():
    global tintors1
    for a in tintors1 : a.color = (choice(kapla_colors))

def tintors2_update():
    global tintors2
    for a in tintors2 : a.color = (choice(kapla_colors))

def tintors3_update():
    global tintors3
    for a in tintors3 : a.color = (choice(kapla_colors))


##  MAIN ----------------------------------------------------------------------
def main():
    scene_setup()
    c.run()

##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()

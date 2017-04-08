#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

"""simple pyglet animation, ms, 10-2016 """

from player import *

# K1,K2,K3 are real life kapla dimensions in mm
# use float to avoid unexpected results with integer divisions
K1=6.0
K2=11.0
K3=34.0

def Caroucell():
    """
    cell,
    movement fits the extents dimensions N,S,E,W (north, south east, west)
    """
    # rectangle cross -----------------------------------------------------
    #  _|_
    #   |
    pt = Point()

    r1 = Rect(N=K3, W=K2).translate(-K2/2, K2/2)  # top |
    r2 = Rect(N=K3, W=K2).translate(-K2/2, -K3-K2/2)  # bottom |
    r3 = Rect(N=K2, W=K3).translate(-K3-K2/2, -K2/2)  # left _
    r4 = Rect(N=K2, W=K3).translate(K2/2, -K2/2)  # right _
    return (pt,r1,r2,r3,r4)

def HiddenMechanics():
    """

    hidden mechanism behind the scene with same args, goes on a toggle layer
    """
    return (Circle(point=(K3+K2/2,K2/2), color=black))


def Stack(self, pos=(0,0,0), width=1, height=1, *args):
    stacks = [y for y in args]
    # for y in stacks:recs = Rect((0,y),(self.width,y))                     TODO
    ####################################################################### TODO
    # body color recs -------------------------------------------------------------
    r1 = Rect(N=12, W=33)
    r2 = Rect(N=12, W=33)
    r3 = Rect(N=12, W=33)
    return (r1,r2,r3)

# svg body mask ---------------------------------------------------------------
body = Shape(visible=True) ## empty shape
filename = "mask.svg"
s = SVG(filename)
s.anchor_x, s.anchor_y = 'center', 'center'
test = SVGshape(svg=s, shape=body)
body.scale = 150 / (s.height * 0.5)
body.pos = (0, 0)

# caroucell -------------------------------------------------------------------
cc = Shape(visible=True, scale=1)
cc += Caroucell()
cc.move(-0, -0)  # move aside half a cell

bodycolor = Shape(visible=True, scale=1)
bodycolor += Stack()
bodycolor.move(-30, 20)  # move aside half a cell

# actions ---------------------------------------------------------------------
sr = SimpleRotation(cc)
####################################################################### TODO

# later -----------------------------------------------------------------------
####################################################################### TODO



# hidden mechanics ------------------------------------------------------------
mecha = Shape(visible=False, scale=1)
mecha.toggles()
mecha +=HiddenMechanics
mecha.move(0, 0)

##  MAIN ----------------------------------------------------------------------
if __name__ == "__main__":
    canvas.target_scale = 100
    canvas.run()


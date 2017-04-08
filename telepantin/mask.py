#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

"""simple pyglet animation, ms, 10-2016 """

from engine import *

# K1,K2,K3 are real life kapla dimensions in mm
# use float to avoid unexpected results with integer divisions
K1=6.0
K2=11.0
K3=34.0

class Caroucell(object):
    """
    cell,
    movement fits the extents dimensions N,S,E,W (north, south east, west)
    """

    def __init__(self, layer=layer_0):
        # rectangle cross -----------------------------------------------------
        #  _|_
        #   |
        pt = Point(layer=layer)

        r1 = Rect(N=K3, W=K2, layer=layer).translate(-K2/2, K2/2)  # top |
        r2 = Rect(N=K3, W=K2, layer=layer).translate(-K2/2, -K3-K2/2)  # bottom |
        r3 = Rect(N=K2, W=K3, layer=layer).translate(-K3-K2/2, -K2/2)  # left _
        r4 = Rect(N=K2, W=K3, layer=layer).translate(K2/2, -K2/2)  # right _

        # movement ------------------------------------------------------------
        sr = SimpleRotation(target=layer)
        canvas.actions.append(sr)

        # observers -----------------------------------------------------------
        o1 = reverse_dir(target=r1)  # check if r1 has gone reverse
        o2 = reverse_dir(target=r2)  # check if r2 has gone reverse
        canvas.observers.extend((o1, o2))


class HiddenMechanics(object):
    """
    hidden mechanism behind the scene with same args, goes on a toggle layer
    """

    def __init__(self, layer=layer_0):
        # shapes
        c1 = Circle(point=(K3+K2/2,K2/2), layer=layer, color=color.black)
        # movement


# body color recs -------------------------------------------------------------
layer_bodycolor = Layer(visible=True, scale=1)
r1 = Rect(N=12, W=33, layer=layer_bodycolor)
r2 = Rect(N=12, W=33, layer=layer_bodycolor)
r3 = Rect(N=12, W=33, layer=layer_bodycolor)
layer_bodycolor.move(-30, 20)  # move aside half a cell

# svg body mask ---------------------------------------------------------------
layer_body = Layer(visible=True)
filename = "mask.svg"
s = SVG(filename)
s.anchor_x, s.anchor_y = 'center', 'center'
test = SVGshape(svg=s, layer=layer_body)
layer_body.scale = 150 / (s.height * 0.5)
layer_body.pos = (0, 0)

# caroucell -------------------------------------------------------------------
layer_caroucell = Layer(visible=True, scale=1)
cc = Caroucell(layer=layer_caroucell)
layer_caroucell.move(-0, -0)  # move aside half a cell

# hidden mechanics ------------------------------------------------------------
layer_mecha = Layer(visible=False, scale=1)
layer_mecha.toggles()
him=HiddenMechanics(layer=layer_mecha)
layer_mecha.move(0, 0)

##  MAIN ----------------------------------------------------------------------
if __name__ == "__main__":
    canvas.target_scale = 100
    canvas.run()


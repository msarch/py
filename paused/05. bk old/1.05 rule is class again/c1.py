#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev105
'''
#--- IMPORTS ------------------------------------------------------------------
import bw
from bw import *

#--- SCENE --------------------------------------------------------------------
p1=Peg(-100,0,0)
p2=Peg(50,50,0) # TODO : check if Peg concept is necessary. Replace w Point?
# shapes are added to an ordered list and displayed FIFO
b = Blip()
#l= line (p1,p2) # pr just p2 if p1 = 0  # TODO
r = Rect (100, 300) # or just p2 if p1 = 0
k = Kapla(blue).peg_to(p2)
#s = Ghost(Color.blue).offset(0,0)
#r = k + Rect(100,100, Color.red) + k.offset(100,0) # TODO

#add peg to shapes : namedtuple(x, y, angle, vx, vy, av)
set_field_color(orange)
b.peg_to(dk)
r.peg_to(p2)  # TODO : make possible to give either 2 or 3 coord or peg


#--- RULES --------------------------------------------------------------------
# ordrered list of rules.
# syntax : name, target shape(s) = TODO), rule args,
Step(shape=r,dx=200,dy=20)
Spin(shape=r,av=10)
Bounce(shape=r,rec=SCREEN)

        #randomize_color((Kapla_colors,10),[k])
        #])

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    animate()
    # export(duration)  # frames are saved to disk

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * july 2014 * bw-rev104
'''

##---IMPORTS-------------------------------------------------------------------
from . rules import Rule

##--- MOVE RULE ---------------------------------------------------------------
class Move(Rule):
    # TODO : replace with general matrix transform
    def tick(self,dt,cell):
        #_print ('  *** Move Rule ......................................... dt = ',dt)
        cell.angle += cell.va * dt
        cell.posx += cell.vx * dt
        cell.posy += cell.vy * dt

##--- BOUNCE RULE -------------------------------------------------------------
class Bounce(Rule):
    def init(self,minx,miny,maxx,maxy):
        # hack to retrieve name
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def tick(self,dt,cell):
        if (cell.posx - cell.shape.aabb[0] < self.minx or \
                cell.shape.aabb[2] + cell.posx > self.maxx):
            # if bounce, reverse speed and move once
            cell.vx *= -1.0
            cell.posx += cell.vx * dt
            cell.posy += cell.vy * dt
            # cell.color = choice(kapla_colors)      # change clr
        elif (cell.posy - cell.shape.aabb[1] < self.miny or \
                cell.shape.aabb[3] + cell.posy > self.maxy):
            # if bounce, reverse speed, move once
            cell.vy *= -1.0
            # TODO dispatch flag cell.bounce =1
            cell.posx += cell.vx * dt
            cell.posy += cell.vy * dt
        else :
            pass

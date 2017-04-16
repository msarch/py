#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
BW / FIELD :: rev_103 :: JUN2014 :: msarch@free.fr
'''

##---IMPORTS-------------------------------------------------------------------
from .. debug import db_print
from . rules import Rule

##--- MOVE RULE ---------------------------------------------------------------
class Move(Rule):
    # TODO : replace with general matrix transform
    def tick(self,dt,cell):
        #db_print ('  *** Move Rule ......................................... dt = ',dt)
        cell.angle += cell.va * dt
        cell.posx += cell.vx * dt
        cell.posy += cell.vy * dt
        db_print ('    * moved Cell : ',cell)
        db_print ('    * pos :', cell.posx, cell.posy)
        db_print('    * speed : ', cell.vx, cell.vy)


##--- BOUNCE RULE -------------------------------------------------------------
class Bounce(Rule):
    def init(self,minx,miny,maxx,maxy):
        # hack to retrieve name
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        db_print('created Bounce rule :',
                self,
                'limits are : ',
                self.minx, self.miny ,self.maxx, self.maxy)

    def tick(self,dt,cell):
        db_print ('  *** Bounce Rule ............................... dt = ',dt)
        if (cell.posx - cell.shape.aabb[0] < self.minx or \
                cell.shape.aabb[2] + cell.posx > self.maxx):
            # if bounce, reverse speed and move once
            cell.vx *= -1.0
            cell.posx += cell.vx * dt
            cell.posy += cell.vy * dt
            db_print('    * reversed x velocity of : ',cell)
            # cell.color = choice(kapla_colors)      # change clr
        elif (cell.posy - cell.shape.aabb[1] < self.miny or \
                cell.shape.aabb[3] + cell.posy > self.maxy):
            # if bounce, reverse speed, move once
            cell.vy *= -1.0
            # TODO dispatch flag cell.bounce =1
            cell.posx += cell.vx * dt
            cell.posy += cell.vy * dt
            db_print ('    * reversed y velocity of cell :', cell)
        else :
            pass
            db_print('    * no bounce, Cell :', cell)
        db_print ('    * pos :', cell.posx, cell.posy)
        db_print('    * speed : ', cell.vx, cell.vy)
        db_print ('  *** end of Bounce Rule .................................')

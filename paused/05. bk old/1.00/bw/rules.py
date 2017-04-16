#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
zululand/rules :: rev_24 :: JUN2014 :: msarch@free.fr
'''

##---IMPORTS-------------------------------------------------------------------
from debug import db_print

##---CONSTANTS-----------------------------------------------------------------
##---VARIABLES-----------------------------------------------------------------



##---CLASS RULE---------------------------------------------------------------
class Rule(object):
    ''' Stores the position, orientation, shape, rule of a cell
    '''
    # TODO : READ
        # http://stackoverflow.com/questions/6535832/python-inherit-the-superclass-init/6535884#6535884
        # http://stackoverflow.com/questions/3782827/why-arent-pythons-superclass-init-methods-automatically-invoked
    def tick(self,dt):
        pass

    def add(self,cell):
        self.cells.append(cell)

##---OTHER RULES---------------------------------------------------------------
class Bounce(Rule):

    def __init__(self,minx,miny,maxx,maxy):
        self.cells = []
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        db_print('created Bounce rule, limits are : ',
                self.minx, self.miny ,self.maxx, self.maxy)

    def tick(self,dt):
        for cell in self.cells:
            db_print ('checking Bounce for actor #',cell)
            if (cell.minx + cell.posx < self.minx or \
                    cell.maxx + cell.posx > self.maxx):  # if bounce,
                cell.vx *=-1
                cell.posx += dt*cell.vx
                cell.posy += dt*cell.vy
                db_print (cell.minx,cell.posx,self.minx)
                db_print ('reverse x dir')
                # cell.color = choice(kapla_colors)      # change clr
            if (cell.miny + cell.posy < self.miny or \
                    cell.maxy + cell.posy > self.maxy):  # if bounce,
                cell.vy *=-1
                cell.posx += dt*cell.vx
                cell.posy += dt*cell.vy
                db_print (cell.minx,cell.posx,self.minx)
                db_print ('reverse x dir')


class Move(Rule):

    def __init__(self,**kwargs):
        ''' a kw for delta angle, dx & dy for displacement '''
        self.cells = []
        db_print(kwargs)
        for i in kwargs:
            setattr(self,i,kwargs[i])

    def tick(self,dt):
        for cell in self.cells:
            db_print ('applying std_move for actor #',cell)
            cell.angle +=cell.va*dt
            cell.posx+=cell.vx*dt
            cell.posy+=cell.vy*dt


class Lifespan(Rule):
    ''' Timetable or scenario class
    - keeps track for every rule of a start and end time for each cell
    - can be dict read from text file
    '''
    pass


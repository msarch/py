#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
BW / FIELD :: rev_102 :: JUN2014 :: msarch@free.fr
'''

##---IMPORTS-------------------------------------------------------------------
from traceback import extract_stack

from debug import db_print
import debug

##--- VARIABLES ---------------------------------------------------------------

##--- FIELD RULES -------------------------------------------------------------
class Rule(object):
    ''' Stores the position, orientation, shape, rule of a cell
    '''
    # rules and concerned cells are stacked in 2 paralel lists

    def tick(self,dt):
        pass

    def __repr__(self):
        return (self.defined_name)


##---OTHER RULES---------------------------------------------------------------
class Bounce(Rule):

    def __init__(self,minx,miny,maxx,maxy):
        # hack to retrieve name
        (filename,line_number,function_name,text)=extract_stack()[-2]
        self.defined_name = text[:text.find('=')].strip()
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        #db_print('created Bounce rule :', self, 'limits are : ', self.minx, self.miny ,self.maxx, self.maxy)


    def tick(self,dt,cell):
        #db_print ('  *** Bounce Rule ....................................... dt = ',dt)
        if (cell.shape.posx - cell.shape.minx < self.minx or \
                cell.shape.maxx + cell.shape.posx > self.maxx):
            # if bounce, reverse speed and move once
            cell.shape.vx *= -1.0
            cell.shape.posx += cell.shape.vx * dt
            cell.shape.posy += cell.shape.vy * dt
            #db_print('    * reversed x velocity of : ',cell)
            # cell.color = choice(kapla_colors)      # change clr
        elif (cell.shape.posy - cell.shape.miny < self.miny or \
                cell.shape.maxy + cell.shape.posy > self.maxy):
            # if bounce, reverse speed, move once
            cell.shape.vy *= -1.0
            cell.shape.posx += cell.shape.vx * dt
            cell.shape.posy += cell.shape.vy * dt
            #db_print ('    * reversed y velocity of cell :', cell)
        else :
            pass
            #db_print('    * no bounce, Cell :', cell)
        #db_print ('    * pos :', cell.shape.posx, cell.shape.posy)
        #db_print('    * speed : ', cell.shape.vx, cell.shape.vy)
        #db_print ('  *** end of Bounce Rule ................................')

class Move(Rule):
    # TODO : replace with general matrix transform
    def __init__(self,**kwargs):
        ''' a kw for delta angle, dx & dy for displacement
        '''
        # hack to retrieve name
        (filename,line_number,function_name,text)=extract_stack()[-2]
        self.defined_name = text[:text.find('=')].strip()
        #db_print('created Move rule.')

    def tick(self,dt,cell):
        #db_print ('  *** Move Rule ......................................... dt = ',dt)
        cell.shape.angle += cell.shape.va * dt
        cell.shape.posx += cell.shape.vx * dt
        cell.shape.posy += cell.shape.vy * dt
        #db_print ('    * moved Cell : ',cell)
        #db_print ('    * pos :', cell.shape.posx, cell.shape.posy)
        #db_print('    * speed : ', cell.shape.vx, cell.shape.vy)
        #db_print ('  *** end of Move Rule ..................................')

class Lifespan(Rule):
    ''' Timetable or scenario class
    - keeps track for every rule of a start and end time for each cell
    - can be dict read from text file
    '''
    pass





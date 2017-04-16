#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/cell :: rev_23 :: MAY2014 :: msarch@free.fr

##---IMPORTS-------------------------------------------------------------------
import pyglet
from debug import db_print

##---CONSTANTS-----------------------------------------------------------------
##---VARIABLES-----------------------------------------------------------------

##---CLASS Field---------------------------------------------------------------
class Field():

    def __init__(self):
        self.duration = 70
        self.scene_folder = ""
        self.cells=[]
        self.rules=[]  # @TODO: rule is a DICT --> name : list of cells
        self.background_color = (0.95, 0.95, 0.95, 0)  # background
        self.current_frame_number = 0  # frame counter
        self.chrono = 0.0  # keeps track of total time elapsed

    def display(self,cell):
        self.cells.append(cell)
        db_print(cell, 'added to', self, 'cells')

    def eval(self,rule):
        self.rules.append(rule)
        db_print(rule, 'added to', self, 'rules')
        db_print('rules cells =', rule.cells)

##---CLASS Cell----------------------------------------------------------------
class Cell(object):
    "Stores the position, orientation, shape, rule of a cell"

    def __init__(self,
            shape=None,
            anchorx=0.0,
            anchory=0.0,
            angle=0.0,
            drawable=True,
            layer=0,
            **kwargs):
        self.shape = shape
        self.anchorx = anchorx
        self.anchory = anchory
        self.angle = angle
        if self.shape:
            self.drawable = drawable
        else:
            self.drawable= False
        self.layer = layer


    def paint(self):
        if self.shape:
            if self.drawable:
                pyglet.gl.glPushMatrix()
                pyglet.gl.glTranslatef(self.anchorx, self.anchory, 0)
                pyglet.gl.glRotatef(self.angle, 0, 0, 1)
                batch = self.shape.get_batch()
                batch.draw()
                pyglet.gl.glPopMatrix()
            else:
                print 'cell', self, 'not drawn'
        else:
            print 'cell', self, 'has no shape'


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

class Move(Rule):

    def __init__(self,**kwargs):
        self.cells = []
        db_print(kwargs)
        for i in kwargs:
            setattr(self,i,kwargs[i])

    def tick(self,dt):
        for cell in self.cells:
            db_print ('applying std_move for actor #',cell)
            cell.angle +=self.a
            cell.anchorx+=self.dx
            cell.anchory+=self.dy


##---CLASS Time Table----------------------------------------------------------

class Lifespan(Rule):
    ''' Timetable or scenario class
    - keeps track for every rule of a start and end time for each cell
    - can be dict read from text file
    '''
    pass


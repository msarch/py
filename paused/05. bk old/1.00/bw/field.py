#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
zululand/field :: rev_24 :: JUN2014 :: msarch@free.fr
'''

##---IMPORTS-------------------------------------------------------------------
import pyglet
from debug import db_print

##---CONSTANTS-----------------------------------------------------------------
##---VARIABLES-----------------------------------------------------------------

##---CLASS Field---------------------------------------------------------------
class Field():

    def __init__(self):
        self.duration = 3
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
            posx=0.0,
            posy=0.0,
            angle=0.0,
            drawable=True,
            layer=0,
            vx=0,
            vy=0,
            va=0,  # angular velocity
            **kwargs):
        self.shape = shape
        self.posx = posx
        self.posy = posy
        self.angle = angle
        self.drawable=drawable
        self.layer=layer
        self.vx=vx
        self.vy=vy
        self.va=va  # angular velocity

        for i in kwargs:
            setattr(self,i,kwargs[i])
        if self.shape==None:
            self.drawable = False
            self.minx.self.maxx,self.miny,self.may = 0,0,0,0
        else:
            (self.minx,self.miny,self.maxx,self.maxy) = self.shape.get_aabb()
            print self.minx,self.miny,self.maxx,self.maxy

    def paint(self):
        if self.shape:
            if self.drawable:
                pyglet.gl.glPushMatrix()
                pyglet.gl.glTranslatef(self.posx, self.posy, 0)
                pyglet.gl.glRotatef(self.angle, 0, 0, 1)
                batch = self.shape.get_batch()
                batch.draw()
                pyglet.gl.glPopMatrix()
            else:
                print 'cell', self, 'not drawn'
        else:
            print 'cell', self, 'has no shape'




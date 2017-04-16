#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * july 2014 * bw-rev104
'''

##---IMPORTS ------------------------------------------------------------------
from traceback import extract_stack
from pyglet.gl import *
from .. field import Field

#--- CONSTANTS ----------------------------------------------------------------

class Peg():
    def __init__(self, x=0, y=0):
        self.x=x
        self.y=y

#--- Cell (Field objects) -----------------------------------------------------
class Cell(object):
    "Stores the data of a field object"
    def __init__(self,
            shape=None,
            defined_name=None,
            posx=0.0,
            posy=0.0,
            angle=0.0,
            vx=0.0,
            vy=0.0,
            va=0.0,
            drawable=True):
        self.shape=shape
        self.defined_name=defined_name
        self.posx = posx*1.0
        self.posy = posy*1.0
        self.angle = angle*1.0
        self.vx=vx*1.0
        self.vy=vy*1.0
        self.va=va*1.0  # angular velocity
        self.drawable=drawable

        if self.drawable:
            Field.display_stack.append(self)
        # hack to retrieve name
        if self.defined_name == None:
            (filename,line_number,function_name,text)=extract_stack()[-2]
            self.defined_name = text[:text.find('=')].strip()


    def __repr__(self):
        return (self.defined_name)

    def paint(self):
        if self.drawable:
            glPushMatrix()
            glTranslatef(self.posx, self.posy, 0)
            glRotatef(self.angle, 0, 0, 1)
            batch = self.shape.get_batch()
            batch.draw()
            glPopMatrix()
        else:
            print 'cell', self, 'is not drawable'

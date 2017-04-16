#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
BW / ENGINE :: rev_103 :: JUN2014 :: msarch@free.fr

this is the pyglet engine.
will cycle trhrough cells for display
will cycle trough rules at each clock tick
will write pics to disk if EXPORT mode is on
'''

##---IMPORTS ------------------------------------------------------------------
import os
from traceback import extract_stack
import pyglet
import pyglet.gl
from pyglet.gl import *
from debug import db_print

#--- CONSTANTS ----------------------------------------------------------------
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
            Field.display_list.append(self)
        # hack to retrieve name
        if self.defined_name == None:
            (filename,line_number,function_name,text)=extract_stack()[-2]
            self.defined_name = text[:text.find('=')].strip()

        db_print('Cell added to Field : ', self)

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
            db_print(self, 'drawn')
        else:
            print 'cell', self, 'is not drawable'


#--- FIELD (singleton) --------------------------------------------------------
class Field():
    display_list = []  # shape list
    rule_stack = []    # rule list
    cell_stack = []    # cell list, 1 cell corresponds to 1 rule in rule list
    paused = False
    current_frame_number = 0  # frame counter
    chrono = 0.0  # keeps track of total time elapsed
    show_fps = True
    duration = 0.0
    # TODO view_size = get_display_size()
    # TODO view_center = get_view_center()


    @classmethod
    def get_display_size(cls):
        _platform = pyglet.window.get_platform()
        _display = _platform.get_default_display()
        _screen = _display.get_default_screen()
        _w = _screen.width
        _h = _screen.height
        return (_w,_h)

    @classmethod
    def get_display_center(cls):
        return((get_display_size)*0.5)


def bind(rule, cell):
    Field.rule_stack.append(rule)
    Field.cell_stack.append(cell)
    db_print('rule/cell', rule, cell, 'added to Field')

#glLoadIdentity()
#glPushMatrix()
#glTranslatef(0,0,0)  # move scene center here?
#glPopMatrix()

def set_background(color):
    glClearColor(color[0]/255.00, color[0]/255.00, color[0]/255.00, 0.00)

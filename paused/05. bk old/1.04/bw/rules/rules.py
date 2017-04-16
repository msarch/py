#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * july 2014 * bw-rev104
'''

##---IMPORTS-------------------------------------------------------------------
from traceback import extract_stack
from . import *

##--- VARIABLES ---------------------------------------------------------------

##--- FIELD RULES -------------------------------------------------------------
class Rule(object):
    ''' Stores the position, orientation, shape, rule of a cell
    '''
    # rules and concerned cells are stacked in 2 paralel lists

    def __init__(self,*args,**kwargs):
        # hack to retrieve name
        (filename,line_number,function_name,text)=extract_stack()[-2]
        self.defined_name = text[:text.find('=')].strip()
        self.active = True
        self.cell_stack=[]  # TODO : maybe use a dict later for ordering
        self.init(*args,**kwargs)

    def tick(dt):
        pass

    def bind(self,cell):
        self.cell_stack.append(cell)

    def init(self,*args,**kwargs):
        pass

    def __repr__(self):
        return (self.defined_name)

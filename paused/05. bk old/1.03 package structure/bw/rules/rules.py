#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
BW / FIELD :: rev_103 :: JUN2014 :: msarch@free.fr
'''

##---IMPORTS-------------------------------------------------------------------
from traceback import extract_stack
from .. debug import db_print
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
        self.init(*args,**kwargs)

    def tick(dt):
        pass

    def init(self,*args,**kwargs):
        pass

    def __repr__(self):
        return (self.defined_name)

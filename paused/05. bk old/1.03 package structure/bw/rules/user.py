#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
BW / FIELD :: rev_103 :: JUN2014 :: msarch@free.fr
'''

##---IMPORTS-------------------------------------------------------------------
from ..debug import db_print
from . rules import Rule
##---OTHER RULES---------------------------------------------------------------

class Lifespan(Rule):
    ''' Timetable or scenario class
    - keeps track for every rule of a start and end time for each cell
    - can be dict read from text file
    '''
    pass

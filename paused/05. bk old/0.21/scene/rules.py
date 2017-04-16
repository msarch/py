#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/bw/rules :: rev 21 :: MAY2014 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from debug import db_print

def rule1(actor,dt):
    db_print ('applying rule1 for actor #',actor)
    actor.angle +=1

def rule2(actor,dt):
    db_print ('applying rule2 for actor #',actor)
    actor.anchorx+=0.5

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/scene/creature1 :: rev 20 :: MAY2014 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from actor import Actor
from shapes import s
from rules import rule1, rule2
from debug import db_print

#-ACTOR SUBCLASS---------------------------------------------------------------



# TODO : what if rule for many?
# TODO : where is DATA stored ???
        # i.e. : number of actors, gradient or forces field...
        # here acces to other actors publications, position

g=Actor(shape=s,ruleset=[rule2])



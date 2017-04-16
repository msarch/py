#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/scene/creature1 :: rev 22 :: MAY2014 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from field import Actor
from shapes import s2
from rules import rule1, rule2
from debug import db_print

#-ACTOR SUBCLASS---------------------------------------------------------------
# TODO : what if rule for many?
# TODO : where is DATA stored ???
        # i.e. : number of actors, gradient or forces field...
        # here acces to other actors publications, position



h=Actor(shape=s2,ruleset=[rule1,rule2])


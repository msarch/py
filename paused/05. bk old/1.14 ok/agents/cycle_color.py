#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# msarch@free.fr * jan 2015 * bw-rev113

##--- IMPORTS -----------------------------------------------------------------
from itertools import cycle
from agents.agent import Agent, broadcast

class Cycle_Color(Agent):
    def setup(self):
        self.i = cycle(self.color_list)
        self.t = cycle(self.targets)
    def tick(self, dt):
        t = self.t.next()
        i = self.i.next()
        t.color = i
        t.batch=None
# remember to erase batch if shape has changed or make a color setter in shape  TODO
cycle_color = Cycle_Color

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev107 * striped down

this is the pyglet engine.
- displays cells on windows redraws
- cycle through rules at each clock tick
'''

##---IMPORTS ------------------------------------------------------------------
import cells

#--- run mode options 1 : fullscreen animation --------------------------------
def start():
    print cells.set
    cells.paint()



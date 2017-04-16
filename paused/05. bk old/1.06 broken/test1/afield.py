#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from acells import Cell


def draw():
    Cell.paint_all()
    print 'drawn'



#--- run mode options 1 : fullscreen animation --------------------------------
if __name__ == "__main__":

    Cell('c1', shape='b1')
    print 'Cell.lmnts seen from field main', Cell.lmnts, Cell.ll
    draw()



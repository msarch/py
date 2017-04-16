#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from collections import OrderedDict
##---GENERAL GRAPHIC shape CLASS-----------------------------------------------
class Cell(object):

    lmnts = []
    ll = OrderedDict()
    def __init__(self, name, **kwargs):

        self.name=name
        print 'self class:', self.__class__
        Cell.lmnts.append(self)
        Cell.ll[self.name] = self




        print ""
        print ":: Cell lmnts is :"
        print Cell.lmnts


    @classmethod
    def paint_all(cls):
        print ' cls.lmnts seen from paint_all() classmethod :', cls.lmnts
        print 'Cell.ll seen from paint_all() classmethod', Cell.ll

        for cell in cls.lmnts:
            if hasattr(cell,'shape'):
                print 'paint me', cell.shape


if __name__ == "__main__":

    Cell('c1', shape='b1')
    print 'Cell.lmnts seen from main', Cell.lmnts
    print 'Cell.ll seen from main', Cell.ll

    Cell.paint_all()

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-


r=1

class setup():
    r=2

def pr():
    print r
    print setup.r



##-----------------------------------------------------------------------------
if __name__ == "__main__":
    ''' init of a new pyglet window setup, and run
    '''
    pr()
    setup.r=3
    pr()


    #export(f,duration=3.5)


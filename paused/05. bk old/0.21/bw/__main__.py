#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/main :: rev 21 :: MAY2014 :: msarch@free.fr

##---IMPORTS-------------------------------------------------------------------
from field import Field
from gui import Engine

##---MAIN----------------------------------------------------------------------
def main():
    e = Engine()
    Field.init()
    e.run()

##-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

##---NOTES---------------------------------------------------------------------
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
'''

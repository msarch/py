#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 20 :: 05.2014 :: msarch@free.fr

##---IMPORTS-------------------------------------------------------------------
import os
import sys

from engine import Engine
from scene import Scene
from debug import db_print


##---MAIN----------------------------------------------------------------------
def main():
    fn = sys.argv[1]
    db_print ('user folder is :',fn)
    if os.path.exists(fn):
        db_print (os.path.basename(fn),'exists')  # file exists
        s = Scene(fn)
        e = Engine(s, duration=70)
        e.run()

##-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

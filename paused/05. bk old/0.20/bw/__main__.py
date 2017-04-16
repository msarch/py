#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/main :: rev 20 :: MAY2014 :: msarch@free.fr

##---IMPORTS-------------------------------------------------------------------
import os
import sys
from glob import glob
from imp import load_source
from engine import Engine
from actor import Actor
from debug import db_print


##--- CONSTANTS AND VARIABLES -------------------------------------------------

##---ACTORS FOLDER PARSING-----------------------------------------------------
def parse_folder(scene_folder):
    db_print('getting modules from :',scene_folder)

    sys.path.insert(0,scene_folder)  # include scene folder

    for path in glob(scene_folder+'/[!_]*.py'):
        db_print('trying to load :',path)
        name, ext = os.path.splitext(os.path.basename(path))
        mdl = load_source(name, path)
        db_print (name, 'is loaded')
        db_print (mdl)

##---MAIN----------------------------------------------------------------------
def main():
    fn = sys.argv[1]
    # TODO : use getopt?
    db_print ('user folder is :',fn)
    if os.path.exists(fn):
        db_print (os.path.basename(fn),'exists')  # file exists
        parse_folder(fn)
        e = Engine(actors=Actor.registry)
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

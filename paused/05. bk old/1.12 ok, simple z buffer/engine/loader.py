#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * nov 2014 * bw-rev112
'''
##--- IMPORTS -----------------------------------------------------------------
import os
import sys
from glob import glob
from imp import load_source

##--- CONSTANTS AND VARIABLES -------------------------------------------------
DEFAULT_SCENE_FOLDER = 'scene'  # in sibling folder of main folder

##-----------------------------------------------------------------------------
def get_scene_folder():
    '''
    returns the folder given as argument by the user,
    returns the default folder otherwise
    '''
    if len(sys.argv) == 2:
        fn = sys.argv[1]                                        #  use getopt?  TODO
        if os.path.exists(fn):
            print ':: scene folder :', os.path.basename(fn)
            return(fn)
        else:
            print ':: path not found, exiting'
            exit()
    else:  # default scene folder in main folder
        fn = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
             DEFAULT_SCENE_FOLDER))
        print ':: no folder specified, using default :', fn
        return(fn)


def parse_folder(scene_folder):
    ''' loads any .py module located inside scene_folder
    '''
    print '::'
    print ':: parsing :'
    print '::', scene_folder
    print '::'
    sys.path.insert(0, scene_folder)  # include scene folder
    for path in glob(scene_folder+'/[!_]*.py'):
        name, ext = os.path.splitext(os.path.basename(path))
        print':: trying to load : ', name
        print '::'
        mdl = load_source(name, path)
        print '::'
        print '::', name, ' loaded'
        print '::'
    print '::'
    print ':: all modules loaded'
    print '::'

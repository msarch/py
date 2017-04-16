#!/usr/bin/python
# -*- coding: utf-8 -*-

# msarch@free.fr * feb 2015 * bw-rev116

##--- IMPORTS -----------------------------------------------------------------
import os
import sys
from glob import glob
from imp import load_source

##--- CONSTANTS AND VARIABLES -------------------------------------------------
DEFAULT_SCENE_FOLDER = 'scene'  # in sibling folder of main folder

##-----------------------------------------------------------------------------
def get_folder():
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


##-----------------------------------------------------------------------------
def load_scene(f):
    ''' loads any .py module located inside f
    '''
    print '::  parsing folder:', f
    sys.path.insert(0, f)  # include scene folder
    for path in glob(f+'/[!_]*.py'):
        name, ext = os.path.splitext(os.path.basename(path))
        print'::  next is : ', name
        _ = load_source(name, path)
        print '::  ', name, ' loaded'
    print '::  all modules loaded.'




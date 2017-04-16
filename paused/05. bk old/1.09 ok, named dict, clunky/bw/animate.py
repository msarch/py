#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev109
'''
##--- IMPORTS -----------------------------------------------------------------
import os
import sys
from glob import glob
from imp import load_source
import field


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
    print ':: parsing :', scene_folder
    sys.path.insert(0, scene_folder)  # include scene folder
    for path in glob(scene_folder+'/[!_]*.py'):
        name, ext = os.path.splitext(os.path.basename(path))
        print':: trying to load : ', name
        mdl = load_source(name, path)
        print mdl
        print '::', name, ' loaded'
    print ':: all modules loaded'
    print '::'


def splash_screen():
    print "::                          ::"
    print "::                          ::"
    print "::       bw / animate       ::"
    print "::                          ::"
    print "::                          ::"
    print '::'


##--- MAIN --------------------------------------------------------------------
if __name__ == "__main__":
    splash_screen()
    scene_folder = get_scene_folder()
    parse_folder(scene_folder)
    field.start()

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev107
'''
##--- IMPORTS -----------------------------------------------------------------
import os
import sys
from glob import glob
from imp import load_source
import inspect

import filed

##--- CONSTANTS AND VARIABLES -------------------------------------------------
DEFAULT_SCENE_FOLDER ='scene'  #  should be at same path level as main folder

##-----------------------------------------------------------------------------
def get_scene_folder():
    ''' returns the folder specified by the user
    '''
    if len(sys.argv) == 2:
        fn = sys.argv[1]
        # TODO : use getopt?
        if os.path.exists(fn):
            print ""
            print ':: parsing folder :'
            print os.path.basename(fn)  # folder exists
            return(fn)
        else:
            exit()
    else:  # default scene folder in main folder
        fn = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..',
            DEFAULT_SCENE_FOLDER ))
        print ""
        print ':: no folder specified, default folder is :'
        print fn
        return(fn)

def parse_folder(scene_folder):
    ''' Loads al module inside scene_folder
    '''
    print ""
    print ':: getting modules from :'
    print scene_folder

    sys.path.insert(0,scene_folder)  # include scene folder

    for path in glob(scene_folder+'/[!_]*.py'):
        print ""
        print':: trying to load :'
        print path
        name, ext = os.path.splitext(os.path.basename(path))
        mdl = load_source('c1', path)
        print ""
        print ':: module loaded :'
        print name, mdl
    print''
    print 'all modules loaded'

##--- MAIN --------------------------------------------------------------------
if __name__ == "__main__":

    print ""
    print ""
    print "   :::   bw / export   :::"
    print ""
    print ""

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    scene_folder = get_scene_folder()
    parse_folder(scene_folder)
    print sys.path
    filed.start()
    # export(duration)  # frames are saved to disk

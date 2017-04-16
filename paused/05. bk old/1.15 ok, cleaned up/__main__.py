#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * jan 2015 * bw-rev111b
'''
##--- IMPORTS -----------------------------------------------------------------
from engine import loader, loop

##-----------------------------------------------------------------------------
def splash_screen():
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '                    ::::::::::::::::::::::::::::::'
    print '                    ::                          ::'
    print '                    ::                          ::'
    print '                    ::       bw / animate       ::'
    print '                    ::                          ::'
    print '                    ::                          ::'
    print '                    ::::::::::::::::::::::::::::::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'
    print '::'


##--- MAIN --------------------------------------------------------------------
if __name__ == "__main__":
    splash_screen()
    scene_folder = loader.get_scene_folder()
    loader.parse_folder(scene_folder)
    loop.start()

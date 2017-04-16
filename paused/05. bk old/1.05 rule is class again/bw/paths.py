#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev105
'''

#--- IMPORTS ------------------------------------------------------------------

##--- CONSTANTS AND VARIABLES -------------------------------------------------

##---GENERAL GRAPHIC shape CLASS-------------------------------------------
class Path(object):
    """
    Stores a list of vertices, a single color, and a primitive type
    Intended to be rendered as a single OpenGL primitive
    """
    def __init__(self, verts, pathtype = None):
        global setup
        self.verts = verts
        self.pathtype = pathtype


#float bearVelocity = screenSize.width / 3.0;

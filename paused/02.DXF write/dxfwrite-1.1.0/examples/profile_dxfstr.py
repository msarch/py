#!/usr/bin/env python
#coding:utf-8
# Purpose: examples for dxfwrite usage, see also tests for examples
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

__author__ = "mozman <mozman@gmx.at>"

import sys
import os

from timeit import Timer
from random import random

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf
from dxfwrite.util import StringIO

def get_cube(basepoint, length):
    def scale( point ):
        return ( (basepoint[0]+point[0]*length),
                 (basepoint[1]+point[1]*length),
                 (basepoint[2]+point[2]*length))
    pface = dxf.polyface()
    # cube corner points
    p1 = scale( (0,0,0) )
    p2 = scale( (0,0,1) )
    p3 = scale( (0,1,0) )
    p4 = scale( (0,1,1) )
    p5 = scale( (1,0,0) )
    p6 = scale( (1,0,1) )
    p7 = scale( (1,1,0) )
    p8 = scale( (1,1,1) )

    # define the 6 cube faces
    # look into -x direction
    # Every add_face adds 4 vertices 6x4 = 24 vertices
    # On dxf output double vertices will be removed.
    pface.add_face([p1, p5, p7, p3], color=1) # base
    pface.add_face([p1, p5, p6, p2], color=2) # left
    pface.add_face([p5, p7, p8, p6], color=3) # front
    pface.add_face([p7, p8, p4, p3], color=4) # right
    pface.add_face([p1, p3, p4, p2], color=5) # back
    pface.add_face([p2, p6, p8, p4], color=6) # top
    return pface

def simple_faces():
    pface = dxf.polyface()
    p1 = (0,0,0)
    p2 = (0,1,0)
    p3 = (1,1,0)
    p4 = (1,0,0)

    p5 = (0,0,1)
    p6 = (0,1,1)
    p7 = (1,1,1)
    p8 = (1,0,1)

    pface.add_face([p1, p2, p3, p4]) # base
    pface.add_face([p5, p6, p7, p8]) # top
    return pface

print("Profiling dxfstr() speed")

def create_dxf_drawing():
    dwg = dxf.drawing() # create a drawing
    # add the active viewport
    dwg.add_vport(
        '*Active',
        center_point=(0, 0),
        height = 30,
        direction_point=(30, 30, 10)
        )
    for x in range(10):
        for y in range(10):
            dwg.add(get_cube((x,y, random()), random()))
    return dwg

drawing = create_dxf_drawing()

def profile_dxfstr():
    dxf_string = dxfwrite.dxfstr(drawing)

def profile_save_to_fileobj():
    fp = StringIO()
    drawing.save_to_fileobj(fp)
    dxf_string = fp.getvalue()
    fp.close()

setup_dxfstr = """
from __main__ import profile_dxfstr
"""

setup_write_dxf = """
from __main__ import profile_save_to_fileobj
"""

def print_result(time, text):
    print("Operation: %s takes %.2f seconds\n" % (text, time))
    
COUNT = 100
def main():
    print("Sizeof DXF string: %d" % len(dxfwrite.dxfstr(drawing)) )
    t = Timer("profile_dxfstr()", setup_dxfstr)
    print_result(t.timeit(COUNT), 'using the dxfstr()')
    t = Timer("profile_save_to_fileobj()", setup_write_dxf)
    print_result(t.timeit(COUNT), 'using the save_to_fileobj()')

if __name__ == '__main__':
    main()

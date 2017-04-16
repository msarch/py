# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="ckaos"
__date__ ="$Jan 21, 2010 12:41:03 PM$"

from pymt import *

IS_PYMT_PLUGIN = True
PLUGIN_TITLE = 'SVG Viewer'
PLUGIN_AUTHOR = ''
PLUGIN_DESCRIPTION = 'This is an example of Scalable Vector Graphics using the Squirtle library for pyglet.'


def load_svg(fileName,ctx,pos=(0,0)):
    try:
        element = MTScatterSvg(filename = fileName, pos = pos)
        ctx.c.add_widget(element)
    except:
        pass


def pymt_plugin_activate(w, ctx):
    ctx.c = MTKinetic()

    load_svg('/data/Progra/Netbeans/LabGlass/src/test_tube_test.svg',ctx)
    load_svg('/data/Progra/Netbeans/LabGlass/src/buret.svg',ctx,(200,200))
    load_svg('/data/Progra/Netbeans/LabGlass/src/test_tube.svg',ctx)
 
    w.add_widget(ctx.c)

def pymt_plugin_deactivate(w, ctx):
    w.remove_widget(ctx.c)

if __name__ == '__main__':
    w = MTWindow()
    ctx = MTContext()
    pymt_plugin_activate(w, ctx)
    runTouchApp()
    pymt_plugin_deactivate(w, ctx)


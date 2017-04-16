#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * aug 2014 * bw-rev105

this is the pyglet engine.
will cycle trhrough cells for display
will cycle trough rules at each clock tick
will write pics to disk if EXPORT mode is on
'''

##---IMPORTS ------------------------------------------------------------------
import os
from sys import stdout
import pyglet.gl
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key, get_platform
from pyglet.gl import (
    glLoadIdentity, glMatrixMode, gluLookAt, gluOrtho2D,
    GL_MODELVIEW, GL_PROJECTION)
# sub modules
import shapes
import field
import rules

#--- CONSTANTS ----------------------------------------------------------------
MOVIE_FRAMERATE = 1.0 / 25  # framerate for movie export
DT = 1.0/MOVIE_FRAMERATE
# @TODO : check how to go bigger than screen, then resize to fullscreen

#--- Globals ------------------------------------------------------------------
frame = 0  # frame counter
chrono = 0.0  # keeps track of total time elapsed

#--- create_output_dir --------------------------------------------------------
def make_a_dir():
    abspath = os.path.abspath(__file__)
    parent = os.path.dirname(os.path.dirname(abspath))
    imgdir = os.path.join (parent, 'out')
    try:
        os.makedirs(imgdir)
    except OSError:
        pass
    os.chdir(imgdir)

#--- write pic to disk --------------------------------------------------------
def save_a_frame(frame):
    n = str(frame).zfill(5)
    filename = "fr_" + n + '.png'
    pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
    print ' --> ', filename

#--- export image loop ----------------------------------------------------
def export_loop():
    global chrono, frame
    while chrono < movie_duration:
        chrono += DT
        frame += 1
        rules.tick(dt)
        # tick with the constant DT, regardless of real time interval
        # so that even if refresh is slow no frame should be missing
        glClear(GL_COLOR_BUFFER_BIT)
        shapes.paint()
        save_a_frame(frame)
        print(frame)
    print 'done'
    print'image dir is : ', os.getcwd()
    exit(0)

#--- run mode options 2 : file export of image files --------------------------
def export(duration):
    field.view_setup()
    #clock.schedule_interval_soft(export_loop, MOVIE FRAMERATE)
    pyglet.app.run()
    export_loop()


#--- NOTES --------------------------------------------------------------------
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
'''


#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
BW / ENGINE :: rev_103 :: JUN2014 :: msarch@free.fr

this is the pyglet engine.
will cycle trhrough cells for display
will cycle trough rules at each clock tick
will write pics to disk if EXPORT mode is on
'''

##---IMPORTS ------------------------------------------------------------------
import os
from itertools import izip
import pyglet
import pyglet.gl
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key

from field import Field
from debug import db_print
import debug

#--- CONSTANTS ----------------------------------------------------------------
PREVIEW_SIZE = (800, 600)
FRAMERATE = 1.0 / 60  # max display framerate
MOVIE_FRAMERATE = 1.0 / 25  # framerate for movie export

#--- PYGLET ENGINE ------------------------------------------------------------
VIEW = pyglet.window.Window()
FPS_DISP = pyglet.clock.ClockDisplay()
KEY_ACTIONS = {
    key.ESCAPE: lambda: exit(),
    #key.PAGEUP: lambda: Field.camera.zoom(2),
    #key.PAGEDOWN: lambda: Field.camera.zoom(0.5),
    #key.LEFT: lambda: Field.camera.pan(self.camera.scale, -1.5708),
    #key.RIGHT: lambda: Field.camera.pan(self.camera.scale, 1.5708),
    #key.DOWN: lambda: Field.camera.pan(self.camera.scale, 3.1416),
    #key.UP: lambda: Field.camera.pan(self.camera.scale, 0),
    key.SPACE: lambda: toggle_pause(),
    key.D : lambda: toggle_debug(),
    key.F: lambda: toggle_fps_display(),
    key.I : lambda: save_a_frame(),
    }

#--- w init (GL stuff) --------------------------------------------------------
def gl_setup():
    VIEW.set_mouse_visible(False)
    Field.set_background(0.95,0.95,0.95)  # default can be overriden
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def gl_clear():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    #glPushMatrix()
    #glTranslatef(0,0,0)  # move scene center here?
    #glPopMatrix()

def get_display_size():
    _platform = pyglet.window.get_platform()
    _display = _platform.get_default_display()
    _screen = _display.get_default_screen()
    _w = _screen.width
    _h = _screen.height
    return (_w,_h)

def get_display_center():
    return((get_display_size)*0.5)

#--- w paint ------------------------------------------------------------------
@VIEW.event
def on_draw():
    """Clear the current OpenGL context, calls cell's paint_all method
    """
    gl_clear()
    # @TODO : inserer le facteur d'adaptation a la taille de l'ecran,
    # et centrer
    for cell in Field.display_list:
        cell.paint()
    if Field.show_fps:
        FPS_DISP.draw()

#--- w key handling -----------------------------------------------------------
def toggle_pause():
    db_print('toggle_pause')
    Field.paused = (True,False)[Field.paused]

def toggle_debug():
    db_print('toggle_debug')
    debug.DEBUG = (True,False)[debug.DEBUG]

def toggle_fps_display():
    db_print('toggle_fps')
    Field.show_fps = (True,False)[Field.show_fps]

@VIEW.event
def on_key_press(symbol, modifiers):  # override pyglet window's
    if symbol in KEY_ACTIONS:
        KEY_ACTIONS[symbol]()

#--- scene update -------------------------------------------------------------
def tick(dt):
    db_print('************************** Begin Tick                        dt = ', dt)
    if Field.paused:
        pass
    else:
        for rule,cell in izip(Field.rule_stack, Field.cell_stack):
            db_print('*** calling rule :')
            db_print('  * rule : ', rule)
            db_print('  * cell : ', cell)
            db_print('  * dt   : ', dt)
            if rule.active:
                rule.tick(dt,cell)
            else:
                pass
    db_print('**************************** End Tick                        dt = ', dt)

#--- write pic to disk --------------------------------------------------------
def save_a_frame():
    n = str(Field.current_frame_number()).zfill(5)
    filename = "fr_" + n + '.png'
    pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
    print ' --> ', filename

#--- export image loop --------------------------------------------------------
def pic_export_loop(dt):
        # tick at a constant dt, regardless of real time
        # so that even if refresh is slow no frame should be missing
        Field.chrono += dt  #TODO le dt n'est pas fixe !!! a corriger
        if Field.chrono > Field.duration:
            print 'done'
            print'image dir is : ', os.getcwd()
            exit()
        else:
            tick(dt)  # dt is forced as a constant = MOVIE_FRAMERATE
            save_a_frame()
            paint()

#--- run mode options 1 : fullscreen animation --------------------------------
def animate():
    VIEW.set_fullscreen(True)
    # normal loop : run the preview at good rate
    # clock.schedule_interval(paint, FRAMERATE)
    # and try (soft) to run anim at same speed
    clock.schedule_interval(tick, FRAMERATE)
    pyglet.app.run()

#--- run mode options 2 : file export of image files --------------------------
def export(duration):
    VIEW.set_size(PREVIEW_SIZE[0], PREVIEW_SIZE[1])
    # @TODO : check if bigger than screen, then set fullscreen
    # or 80% of screen, print error message
    # then set XMAX,YMAX
    abspath = os.path.abspath(__file__)
    parent = os.path.dirname(os.path.dirname(abspath))
    imgdir = os.path.join (parent, 'out')
    try:
        os.makedirs(imgdir)
    except OSError:
        pass
    os.chdir(imgdir)
    clock.schedule_interval_soft(pic_export_loop, MOVIE_FRAMERATE)
    pyglet.app.run()

#--- NOTES --------------------------------------------------------------------
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
  '''

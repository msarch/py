#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
BW / ENGINE :: rev_102 :: JUN2014 :: msarch@free.fr

this is the pyglet engine.
will cycle trhrough cells for display
will cycle trough rules at each clock tick
will write pics to disk if EXPORT mode is on
'''

##---IMPORTS ------------------------------------------------------------------
import os
from itertools import izip
from traceback import extract_stack

import pyglet
import pyglet.gl
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key

from colors import Color
from debug import db_print
import debug

##---CONSTANTS-----------------------------------------------------------------
PREVIEW_SIZE = (600, 600)
FRAMERATE = 1.0 / 60  # max display framerate
MOVIE_FRAMERATE = 1.0 / 25  # framerate for movie export
w = pyglet.window.Window()
fpsd = pyglet.clock.ClockDisplay()
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



##--- FIELD OBJECTS -----------------------------------------------------------
class Cell(object):
    "Stores the data of a field object"
    def __init__(self, shape=None, defined_name=None, **kwargs):
        self.shape=shape
        self.defined_name=defined_name
        for i in kwargs:
            setattr(self,i,kwargs[i])
        # hack to retrieve name
        if self.defined_name == None:
            (filename,line_number,function_name,text)=extract_stack()[-2]
            self.defined_name = text[:text.find('=')].strip()
        #db_print('Cell added to Field : ', self)

    def __repr__(self):
        return (self.defined_name)

#---WIN key handling-----------------------------------------------------------
class Field():
    display_list = []  # shape list
    rule_stack = []  # rule list
    cell_stack = []  # cell list, tied to rule list
    color = Color.very_light_grey # default color can be overriden
    glClearColor(*color)
    paused = False
    current_frame_number = 0  # frame counter
    chrono = 0.0  # keeps track of total time elapsed
    show_fps = True
    duration = 0.0

    @classmethod
    def bind(cls, rule, cell):
        cls.rule_stack.append(rule)
        cls.cell_stack.append(cell)
        #db_print('rule/cell', rule, cell, 'added to Field')

##---PYGLET ENGINE-------------------------------------------------------------
#---scene paint----------------------------------------------------------------
@w.event
def on_draw():
    """Clear the current OpenGL context, calls cell's paint_all method
    """
    gl_clear()
    # @TODO : INSERER LE FACTEUR D'ADAPTATION A LA TAILLE DE L'ECRAN
    for shape in Field.display_list:
        shape.paint()
    #db_print('Field paint')
    if Field.show_fps:
        fpsd.draw()

#---scene update---------------------------------------------------------------
def tick(dt):
    #db_print('************************** Begin Tick                        dt = ', dt)
    if Field.paused:
        pass
    else:
        #fdt=dt*1.0
        for rule,cell in izip(Field.rule_stack, Field.cell_stack):
            #db_print('*** calling rule :')
            #db_print('  * rule : ', rule)
            #db_print('  * cell : ', cell)
            #db_print('  * dt   : ', dt)
            rule.tick(dt,cell)
    #db_print('**************************** End Tick                        dt = ', dt)

#--- w events -----------------------------------------------------------------
def toggle_pause():
    #db_print('toggle_pause')
    Field.paused = (True,False)[Field.paused]

def toggle_debug():
    #db_print('toggle_debug')
    debug.DEBUG = (True,False)[debug.DEBUG]

def toggle_fps_display():
    #db_print('toggle_fps')
    Field.show_fps = (True,False)[Field.show_fps]

@w.event
def on_key_press(symbol, modifiers):  # override pyglet window's
    if symbol in KEY_ACTIONS:
        KEY_ACTIONS[symbol]()
#---GL stuff-------------------------------------------------------------------

def w_init(fullscreen=True):
    w.set_mouse_cursor(None)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    if fullscreen:
        w.set_fullscreen(True)
    else:
        w.set_size(PREVIEW_SIZE[0], PREVIEW_SIZE[1])


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
    return(_screen.width,_screen.height)




#---write pic to disk----------------------------------------------------------
    def save_a_frame():
        n = str(Field.current_frame_number()).zfill(5)
        filename = "fr_" + n + '.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
        print ' --> ', filename

#---export image loop----------------------------------------------------------
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

#---run mode options are fullscreen animation or file export-------------------

def animate():
    w_init(fullscreen=True)
    # normal loop : run the preview at good rate
    # clock.schedule_interval(paint, FRAMERATE)
    # and try (soft) to run anim at same speed
    clock.schedule_interval(tick, FRAMERATE)
    pyglet.app.run()

def export(duration):
    w_init(fullscreen=false)
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
##---NOTES---------------------------------------------------------------------
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
  '''

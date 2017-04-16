#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: gldisplay :: rev 13-d3 :: 10.2013 :: msarch@free.fr


##  IMPORTS -------------------------------------------------------------------
import zulus
import pyglet
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key

import shapes
from rules import Ruleset
##  CONSTANTS AND VARIABLES ---------------------------------------------------

global DEBUG, END_TIME, ANIM_FRAMERATE, PREVIEW_SIZE, BGGCOLOR, FPS

DEBUG=1
FPS= 60 # display max framerate
PicPS = 25  # EXPORT MODE FRAMERATE : images per second for movie export
END_TIME = 3 # EXPORT MODE : duration (seconds) of the anim
PREVIEW_SIZE =(800,600)
BGCOLOR =shapes.Color.very_light_grey # background

##--- WINDOW ------------------------------------------------------------------
class Engine(pyglet.window.Window):

    def __init__(self,MODE):
        self.mode=MODE
        self.ruleset=Ruleset()
        self.chrono=0.0 # keeps track of total time elapsed
        self.frame_number=0 # frame counter
        self.paused=False
        self.display_fps = pyglet.clock.ClockDisplay()
        pyglet.window.Window.__init__(self,vsync = True)
        # set size depending on choosen mode
        if self.mode=='FULL':
            self.set_fullscreen(True)
            self.get_display_size()
        elif self.mode in ('EXPORT','PREVIEW'): #export or preview  mode
            self.xmax = PREVIEW_SIZE[0]
            self.ymax = PREVIEW_SIZE[1]
            self.set_size(self.xmax,self.ymax)
        else:
            print 'error : undefined mode'
            exit()
        self.key_setup()
        self.print_keys()
        self.gl_setup()
        self.mouse_setup()
    #---key handling-----------------------------------------------------------
    def key_setup(self):
        self.key_actions = {
        key.ESCAPE: lambda: exit(),
        #key.PAGEUP: lambda: self.camera.zoom(2),
        #key.PAGEDOWN: lambda: self.camera.zoom(0.5),
        #key.LEFT: lambda: self.camera.pan(self.camera.scale, -1.5708),
        #key.RIGHT: lambda: self.camera.pan(self.camera.scale, 1.5708),
        #key.DOWN: lambda: self.camera.pan(self.camera.scale, 3.1416),
        #key.UP: lambda: self.camera.pan(self.camera.scale, 0),
        key.SPACE : lambda: self.toggle_pause(),
        key.I : lambda: self.save_a_frame(),
        }

    def print_keys(self):
        print "keys to try:", \
            [key.symbol_string(k) for k in self.key_actions.keys()]

    def on_key_press(self,symbol, modifiers): #override pyglet window's
        if symbol in self.key_actions:
            self.key_actions[symbol]()

    def toggle_pause(self):
        self.paused=(True,False)[self.paused]

    #---mouse handling---------------------------------------------------------
    def mouse_setup(self):
        self.set_mouse_visible(False)

    #---GL stuff---------------------------------------------------------------
    def gl_setup(self):
        # Set the window color, this will be transparent in saved images.
        glClearColor(*BGCOLOR)
        self.gl_clear()
        # use glOrtho and turn off depthwriting and depthtesting
        #glDisable(GL_DEPTH_TEST)
        #glDepthMask(GL_FALSE)
        # Normally glColor specifies values for use when lighting is *off*,
        # and glMaterial specifies values for use when lighting is *on*.
        # Disable lighting and color material features:
        #glDisable(GL_LIGHTING)
        #glDisable(GL_COLOR_MATERIAL)
        #glLoadIdentity() # reset transformation matrix
        # Most of this is already taken care of in Pyglet.
        #glMatrixMode(GL_PROJECTION)
        #glOrtho(0, self.xmax, 0, self.ymax, -1, 1)
        #glMatrixMode(GL_MODELVIEW)
        # Enable line anti-aliasing.
        #glEnable(GL_LINE_SMOOTH)
        # Enable alpha transparency.
        #glEnable(GL_BLEND)
        #glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, \
        #       GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def gl_clear(self):
        glClear(GL_COLOR_BUFFER_BIT)
        #glClear(GL_DEPTH_BUFFER_BIT)
        #glClear(GL_STENCIL_BUFFER_BIT)
        glLoadIdentity()


    def get_display_size(self):
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        self.xmax = screen.width
        self.ymax = screen.height

    #---EXPORT ----------------------------------------------------------------

    def save_a_frame(self):
            file_num=str(self.frame_number).zfill(5)
            file_t=str(self.chrono)
            filename="frame-"+file_num+'-@ '+file_t+'sec.png'
            pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
            print 'image file writen : ',filename

    def export_loop(self,dt):
        constant_interval=1.0/PicPS
        if self.chrono<END_TIME:
            # update at a constant dt, regardless of real time
            # so that even if refresh is slow no frame should be missing
            # self.frame_draw(PicPS)
            self.update(constant_interval)
            self.frame_draw(dt)
            self.frame_number+=1
            self.save_a_frame()
        else:
            exit()

    #---FULLSCREEN AND WINDOWED-PREVIEW MODE loop------------------------------
    def frame_draw(self,dt):
        """Clear the current OpenGL context, reset the model/view matrix and
        invoke the `draw()` methods of the zulus
        """
        if not self.paused:
            self.gl_clear()
            zulus.paint_all()
            if DEBUG:
                self.display_fps.draw()

    def update(self,dt):
        if not self.paused:
            self.chrono+=dt
            self.ruleset.update(dt,self.chrono)
        else:
            pass

    #---run loop options-------------------------------------------------------

    def run(self):
            # schedule pyglet ondraw loop at max framerate
            # and the update function at more than fps
            # frame / time driven loop

        if  self.mode in ('FULL','PREVIEW'):
            clock.schedule_interval(self.frame_draw,1.0/FPS)
            clock.schedule_interval_soft(self.update, 1.0/(1.0*FPS))
        elif self.mode == 'EXPORT': # export loop
            # try to run export method at final anim speed,
            clock.schedule_interval_soft(self.export_loop,1.0/PicPS)
            # anyway run preview at good rate
            clock.schedule_interval_soft(self.frame_draw, 1.0/FPS)

        pyglet.app.run()


#--- FUNCTIONS ----------------------------------------------------------------







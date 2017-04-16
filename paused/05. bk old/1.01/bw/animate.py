#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
ZULULAND / ANIMATE :: rev_24 :: JUN2014 :: msarch@free.fr

this is the pyglet engine.
will cycle trhrough cells for display
will cycle trough rules at each clock tick
will write pics to disk if EXPORT mode is on
'''

##---IMPORTS ------------------------------------------------------------------
import os
import pyglet
import pyglet.gl
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key
from debug import db_print

##---CONSTANTS-----------------------------------------------------------------
PREVIEW_SIZE = (600, 600)
FRAMERATE = 1.0 / 60  # max display framerate
MOVIE_FRAMERATE = 1.0 / 25  # framerate for movie export

##---VARIABLES-----------------------------------------------------------------


##---PYGLET ENGINE-------------------------------------------------------------
class Engine():
    def __init__(self,field,fullscreen):
        self.field = field
        self.fullscreen = fullscreen
        self.paused = False
        self.show_fps = True
        self.clock_display = pyglet.clock.ClockDisplay()

        WIN = pyglet.window.Window()
        WIN.set_mouse_visible(False)
        self.gl_setup()
        self.key_setup()
        WIN.on_key_press = self.on_key_press

        if self.fullscreen :  #window size depends on choosen MODE
            WIN.set_fullscreen(True)
        else: # export or preview  MODE
            # @TODO : check if bigger than screen, then set fullscreen
            # or 80% of screen, print error message
            # then set XMAX,YMAX
            WIN.set_size(PREVIEW_SIZE[0], PREVIEW_SIZE[1])

#---WIN key handling-----------------------------------------------------------
    def key_setup(self):
        self.KEY_ACTIONS = {
            key.ESCAPE: lambda: exit(),
            #key.PAGEUP: lambda: Field.camera.zoom(2),
            #key.PAGEDOWN: lambda: Field.camera.zoom(0.5),
            #key.LEFT: lambda: Field.camera.pan(self.camera.scale, -1.5708),
            #key.RIGHT: lambda: Field.camera.pan(self.camera.scale, 1.5708),
            #key.DOWN: lambda: Field.camera.pan(self.camera.scale, 3.1416),
            #key.UP: lambda: Field.camera.pan(self.camera.scale, 0),
            key.SPACE: lambda: self.toggle_pause(),
            key.D : lambda: self.toggle_debug(),
            key.F: lambda: self.toggle_fps_display(),
            key.I : lambda: self.save_a_frame(),
            }

    def on_key_press(self, symbol, modifiers):  # override pyglet window's
        if symbol in self.KEY_ACTIONS:
            self.KEY_ACTIONS[symbol]()

    def toggle_pause(self):
        global paused
        db_print('toggle_pause')
        self.paused = (True,False)[self.paused]

    def toggle_debug(self):
        debug.DEBUG = (True,False)[debug.DEBUG]

    def toggle_fps_display(self):
        self.show_fps = (True,False)[self.show_fps]

#---GL stuff-------------------------------------------------------------------
    def gl_setup(self):
        # Set the window color, this will be transparent in saved images.
        glClearColor(*self.field.background_color)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def gl_clear(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(300,400,0)
        pyglet.gl.glPopMatrix()

    def get_display_size(self):
        _platform = pyglet.window.get_platform()
        _display = _platform.get_default_display()
        _screen = _display.get_default_screen()
        return(_screen.width,_screen.height)

#---scene paint----------------------------------------------------------------
    def paint_a_frame(self, dt):
        """Clear the current OpenGL context, calls cell's paint_all method
        """
        if not self.paused:
            self.gl_clear()
            self.field.paint()
            if self.show_fps:
                self.clock_display.draw()

#---scene update---------------------------------------------------------------
    def tick(self, dt):
        if self.paused:
            pass
        else:
            self.field.tick(dt)

#---write pic to disk----------------------------------------------------------
    def save_a_frame(self):
        self.field.current_frame_number += 1
        file_num = str(self.field.current_frame_number).zfill(5)
        filename = "fr_" + file_num + '.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
        print ' --> ', filename

#---export image loop----------------------------------------------------------
    def pic_export_loop(self, dt):
            # tick at a constant dt, regardless of real time
            # so that even if refresh is slow no frame should be missing
            self.field.chrono += dt
            if self.field.chrono > self.field.duration:
                print 'done'
                print'image dir is : ', os.getcwd()
                exit()
            else:
                self.tick(dt)  # dt is forced as a constant = MOVIE_FRAMERATE
                self.save_a_frame()
                self.paint_a_frame(dt)

#---run mode options are fullscreen animation or file export-------------------
def animate(field):
    e = Engine(field,fullscreen=True)
    # normal loop : run the preview at good rate
    clock.schedule_interval(e.paint_a_frame, FRAMERATE)
    # and try (soft) to run anim at same speed
    clock.schedule_interval_soft(e.tick, FRAMERATE)
    pyglet.app.run()

def export(field,duration):
    abspath = os.path.abspath(__file__)
    parent = os.path.dirname(os.path.dirname(abspath))
    imgdir = os.path.join (parent, 'out')
    try:
        os.makedirs(imgdir)
    except OSError:
        pass
    os.chdir(imgdir)
    field.duration=duration
    e = Engine(field,fullscreen=False)
    clock.schedule_interval_soft(e.pic_export_loop, MOVIE_FRAMERATE)
    pyglet.app.run()
##---NOTES---------------------------------------------------------------------
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
  '''

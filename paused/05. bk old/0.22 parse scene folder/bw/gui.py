#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/engine :: rev 22 :: MAY2014 :: msarch@free.fr

##---IMPORTS ------------------------------------------------------------------
import pprint
import pyglet
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key
from field import Field
from debug import db_print, DEBUG
import debug


##--- CONSTANTS AND VARIABLES -------------------------------------------------
MODE='FULLSCREEN'  # options are: 'FULLSCREEN'; 'PREVIEW'; 'EXPORT'
PREVIEW_SIZE = (600, 600)
FRAMERATE = 1.0 / 60  # max display framerate
MOVIE_FRAMERATE = 1.0 / 25  # framerate for movie export
DURATION = 70


##---PYGLET ENGINE-------------------------------------------------------------
class Engine(pyglet.window.Window):
    """  pyglet window that does all the update and paint job
    """
    def __init__(self):
        pyglet.window.Window.__init__(self, vsync=True)
        self.background_color = (0.95, 0.95, 0.95, 0)  # background
        self.chrono = 0.0  # keeps track of total time elapsed
        self.frame_number = 0  # frame counter
        self.paused = False
        self.set_mouse_visible(False)
        self.show_fps = True
        self.pcd = clock.ClockDisplay()
        self.key_setup()
        self.gl_setup()

        #---window size depends on choosen mode--------------------------------
        if MODE == 'FULLSCREEN':
            self.set_fullscreen(True)

        elif MODE in ('EXPORT', 'PREVIEW'):  # export or preview  mode
             self.set_size(self.PREVIEW_SIZE[0], PREVIEW_SIZE[1])
        else:
            print 'error : undefined mode'
            exit()

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
        key.SPACE: lambda: self.toggle_pause(),
        key.D : lambda: self.toggle_debug(),
        key.F: lambda: self.toggle_fps_display(),
        key.I : lambda: self.save_a_frame(),
        }
        print "keys to try:"
        [pprint.pprint(key.symbol_string(k)) for k in self.key_actions.keys()]

    def on_key_press(self,symbol, modifiers):  # override pyglet window's
        if symbol in self.key_actions:
            self.key_actions[symbol]()

    def toggle_pause(self):
        self.paused = (True,False)[self.paused]

    def toggle_debug(self):
        debug.DEBUG = (True,False)[debug.DEBUG]

    def toggle_fps_display(self):
        self.show_fps = (True,False)[self.show_fps]

    #---GL stuff---------------------------------------------------------------
    def gl_setup(self):
        # Set the window color, this will be transparent in saved images.
        glClearColor(*self.background_color)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def gl_clear(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

    def get_display_size(self):
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        self.xmax = screen.width
        self.ymax = screen.height

    #---scene paint------------------------------------------------------------
    def frame_paint(self,dt):
        """Clear the current OpenGL context, calls actor's paint_all method
        """
        if not self.paused:
            self.gl_clear()
            Field.paint()
            if self.show_fps:
                self.pcd.draw()

    #---scene update-----------------------------------------------------------
    def tick(self,dt):
        """Calls the actors update_all method until time out
        """
        if not self.paused:
            self.chrono += dt
            if self.chrono > DURATION:
                exit()
            Field.tick(dt)
        else:
            pass

    #---write pic to disk------------------------------------------------------
    def save_a_frame(self):
            self.frame_number+=1
            file_num = str(self.frame_number).zfill(5)
            file_t = str(self.chrono)
            filename = "scene " + self.scene + "-frame " + file_num + \
                       " -@ " + file_t + 'sec.png'
            pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
            print 'image file writen : ', filename

    #---run loop options---------------------------------------------------
    def pic_export_loop(self, dt):
            # tick at a constant dt, regardless of real time
            # so that even if refresh is slow no frame should be missing
            self.tick(dt)  # dt is forced as a constant = MOVIE_FRAMERATE
            self.save_a_frame()
            self.frame_paint(dt)

    def run(self):
        if MODE in ('FULLSCREEN', 'PREVIEW'):  # normal loop
            # run the preview at good rate
            clock.schedule_interval(self.frame_paint, FRAMERATE)
            # and try (soft) to run export method at final anim speed,
            clock.schedule_interval_soft(self.tick, FRAMERATE)
        elif MODE == 'EXPORT':  # trigger the export loop
            clock.schedule_interval_soft(self.pic_export_loop, MOVIE_FRAMERATE)
        pyglet.app.run()

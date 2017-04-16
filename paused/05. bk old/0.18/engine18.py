#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: engine :: rev 16 :: 01.2014 :: msarch@free.fr

##---IMPORTS ------------------------------------------------------------------
import pprint
import pyglet
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key


##---NOT E---------------------------------------------------------------------
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
'''


##---PYGLET ENGINE-------------------------------------------------------------
class Engine(pyglet.window.Window):
    """  pyglet window that does all the update and paint job
    """

    def __init__(self, scene, duration=0):
        pyglet.window.Window.__init__(self, vsync=True)
        self.duration = duration
        self.scene = scene
        #---engine setup-------------------------------------------------------
        # schedule pyglet  loop at max framerate
        # and the tick function at more than fps
        # frame / time driven loop
        _DEBUG = 1
        _PREVIEW_SIZE = (600, 600)
        self.background_color = (0.95, 0.95, 0.95, 0)  # background
        self.framerate = 1.0 / 60  # max display framerate
        self.movie_framerate = 1.0 / 25  # framerate for movie export
        self.mode = 'PREVIEW'  # options are: 'FULL'; 'PREVIEW'; 'EXPORT'
        self.chrono = 0.0  # keeps track of total time elapsed
        self.frame_number = 0  # frame counter
        self.paused = False
        self.show_fps = True
        self.pcd = clock.ClockDisplay()
        self.key_setup()
        self.print_keys()
        self.gl_setup()
        self.mouse_setup()

        #---window size depends on choosen mode--------------------------------
        if self.mode == 'FULL':
            self.set_fullscreen(True)
            self.get_display_size()

        elif self.mode in ('EXPORT', 'PREVIEW'):  # export or preview  mode
            self.xmax = _PREVIEW_SIZE[0]
            self.ymax = _PREVIEW_SIZE[1]
            self.set_size(self.xmax, self.ymax)
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
        key.F: lambda: self.toggle_fps_display(),
        key.I : lambda: self.save_a_frame(),
        }

    def print_keys(self):
        print "keys to try:"
        [pprint.pprint(key.symbol_string(k)) for k in self.key_actions.keys()]

    def on_key_press(self,symbol, modifiers): #override pyglet window's
        if symbol in self.key_actions:
            self.key_actions[symbol]()

    def toggle_pause(self):
        self.paused = (True,False)[self.paused]

    def toggle_fps_display(self):
        self.show_fps = (True,False)[self.show_fps]


    #---mouse handling---------------------------------------------------------
    def mouse_setup(self):
        self.set_mouse_visible(False)

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
        """Clear the current OpenGL context, reset the model/view matrix and
        invoke the `()` methods of the zulus
        """
        if not self.paused:
            self.gl_clear()
            self.scene.paint()

            if self.show_fps:
                self.pcd.draw()

    #---scene update-----------------------------------------------------------
    def tick(self,dt):
        """Updates the scene until time out
        by invoquind the tick methods of the scene
        """
        if not self.paused:
            self.chrono += dt
            print self.chrono
            if self.chrono > self.duration:
                exit()
            self.scene.tick(dt)
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
            self.tick(dt)  # dt is forced as a constant = self.movie_framerate
            self.save_a_frame()
            self.frame_paint(dt)

    def run(self):
        if self.mode in ('FULL', 'PREVIEW'):  # normal loop
            # run the preview at good rate
            clock.schedule_interval(self.frame_paint, self.framerate)
            # and try (soft) to run export method at final anim speed,
            clock.schedule_interval_soft(self.tick, self.framerate)
        elif self.mode == 'EXPORT':  # trigger the export loop
            clock.schedule_interval_soft(self.pic_export_loop, movie_framerate)
        pyglet.app.run()

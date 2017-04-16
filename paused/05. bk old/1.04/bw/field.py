#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * july 2014 * bw-rev104

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
from pyglet.window import key, get_platform
from pyglet.gl import (
    glLoadIdentity, glMatrixMode, gluLookAt, gluOrtho2D,
    GL_MODELVIEW, GL_PROJECTION,
)


#--- CONSTANTS ----------------------------------------------------------------
PREVIEW_SIZE = (800, 600)
FRAMERATE = 1.0 / 60  # max display framerate
MOVIE_FRAMERATE = 1.0 / 25  # framerate for movie export
CLOCKDISPLAY = pyglet.clock.ClockDisplay()
SHOW_FPS = True
_screen = get_platform().get_default_display().get_default_screen()
WIDTH, HEIGHT = _screen.width*1.0 ,_screen.height*1.0
CENTX, CENTY = WIDTH*0.5, HEIGHT*0.5
ASPECT = WIDTH / HEIGHT
SCALE=10
KEY_ACTIONS = {
    key.ESCAPE: lambda: exit(),
    #key.PAGEUP: lambda: camera.zoom(2),
    #key.PAGEDOWN: lambda: camera.zoom(0.5),
    #key.LEFT: lambda: camera.pan(camera.scale, -pi/2),
    #key.RIGHT: lambda: camera.pan(camera.scale, +pi/2),
    key.DOWN: lambda: camera.pan(camera.scale, pi),
    #key.UP: lambda: camera.pan(camera.scale, 0),
    #key.COMMA: lambda: camera.tilt(-1),
    #key.PERIOD: lambda: camera.tilt(+1),
    key.SPACE: lambda: toggle_pause(),
    key.I : lambda: save_a_frame(),
    }
VIEW = pyglet.window.Window()
VIEW.set_mouse_visible(False)

#--- FIELD CLASS --------------------------------------------------------------
class Field():
    display_stack = []  # shape list
    rule_stack = []    # rule list
    paused = False
    current_frame_number = 0  # frame counter
    chrono = 0.0  # keeps track of total time elapsed
    duration = 0.0

#--- VIEW key handling --------------------------------------------------------
    @staticmethod
    @VIEW.event
    def on_key_press(symbol, modifiers):  # override pyglet window's
        if symbol in KEY_ACTIONS:
            KEY_ACTIONS[symbol]()

    @classmethod
    def toggle_pause(cls):
        cls.paused = (True,False)[cls.paused]

    @classmethod
    def focus(cls):
        # Set projection matrix suitable for 2D rendering"
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        #gluOrtho2D( -SCALE * ASPECT, SCALE * ASPECT,-SCALE,SCALE)

        ## Set modelview matrix to move, scale & rotate to camera position"
        #glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        #gluLookAt( CENTX, CENTY, +1.0, CENTX, CENTY, -1.0, 0, 1, 0.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, WIDTH, 0, HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
#--- PYGLET ENGINE ------------------------------------------------------------
    @classmethod
    def redraw(cls, dt):
        """ the current OpenGL context, calls cell's paint_all method
        """
        glClear(GL_COLOR_BUFFER_BIT)
        #camera.update()
        #camera.focus(cls.width, cls.height)

        # @TODO : inserer le facteur d'adaptation a la taille de l'ecran,
        for cell in cls.display_stack:
            cell.paint()
        if SHOW_FPS:
            CLOCKDISPLAY.draw()

#--- scene update -------------------------------------------------------------
    @classmethod
    def tick(cls, dt):
        if cls.paused:
            pass
        else:
            for rule in cls.rule_stack:
                if rule.active:
                    for cell in rule.cell_stack:
                        rule.tick(dt,cell)
                else:
                    pass

#--- write pic to disk --------------------------------------------------------
    @classmethod
    def save_a_frame(cls):
        n = str(cls.current_frame_number()).zfill(5)
        filename = "fr_" + n + '.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
        print ' --> ', filename

#--- export image loop --------------------------------------------------------
    @classmethod
    def pic_export_loop(cls, dt):
            # tick at a constant dt, regardless of real time
            # so that even if refresh is slow no frame should be missing
            cls.chrono += dt  #TODO le dt n'est pas fixe !!! a corriger
            if cls.chrono > Field.duration:
                print 'done'
                print'image dir is : ', os.getcwd()
                exit()
            else:
                cls.tick(dt)  # dt is forced as a constant = MOVIE_FRAMERATE
                cls.save_a_frame()
                cls.redraw()

#--- run mode options 1 : fullscreen animation --------------------------------
    @classmethod
    def animate(cls):
        VIEW.set_fullscreen(True)
        cls.focus()
        # normal loop : run the preview at good rate
        clock.schedule_interval(cls.redraw, FRAMERATE)
        # and try (soft) to run anim at same speed
        clock.schedule_interval(cls.tick, FRAMERATE)
        pyglet.app.run()

#--- run mode options 2 : file export of image files --------------------------
    @classmethod
    def export(cls, duration):
        VIEW.set_size(PREVIEW_SIZE[0], PREVIEW_SIZE[1])
        cls.focus()
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
        clock.schedule_interval_soft(cls.pic_export_loop, MOVIE_FRAMERATE)
        pyglet.app.run()


#--- NOTES --------------------------------------------------------------------
'''
from ThinkingParticles, reuse:
    - IDS/ODS : input data stream, output data stream
    - memory node : allows the storage of any kind of data.
    - IN/OUT volume testing algorithm has been added
    - PSearch node, search the nearest/furthest particle in a specific radius
'''


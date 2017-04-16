#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: pygtools :: rev 13-d2 :: 10.2013 :: msarch@free.fr


##  IMPORTS -------------------------------------------------------------------
import rules
import zulus
import pyglet

from camera import Camera
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key

##  CONSTANTS AND VARIABLES ---------------------------------------------------
max_fps=60
very_light_grey=(0.95, 0.95, 0.95, 0)
bgcolor=very_light_grey


##--- WINDOW ------------------------------------------------------------------
class Land(pyglet.window.Window):
    display_fps = pyglet.clock.ClockDisplay()

    def __init__(self):
        pyglet.window.Window.__init__(self,vsync = True,fullscreen=True)
        self.set_mouse_visible(False)
        self.bgcolor=bgcolor
        self.size_x,self.size_y=self.get_display_size()
        self.center= self.size_x*0.5,self.size_y*0.5
        self.paused=False
        self.camera=Camera((self.center), 0.1)
        self.key_actions = {
            key.ESCAPE: lambda: exit(),
            key.PAGEUP: lambda: self.camera.zoom(2),
            key.PAGEDOWN: lambda: self.camera.zoom(0.5),
            key.LEFT: lambda: self.camera.pan(self.camera.scale, -1.5708),
            key.RIGHT: lambda: self.camera.pan(self.camera.scale, 1.5708),
            key.DOWN: lambda: self.camera.pan(self.camera.scale, 3.1416),
            key.UP: lambda: self.camera.pan(self.camera.scale, 0),
            key.COMMA: lambda: self.camera.tilt(-1),
            key.PERIOD: lambda: self.camera.tilt(+1),
            key.P : lambda: self.toggle_pause(),
            }


        self.gl_setup()
        # schedule the update function at 'fps' times per second
        clock.schedule_interval(self.update, 1.0/100.0)
        clock.set_fps_limit(max_fps)

    def on_key_press(self,symbol, modifiers):
        if symbol in self.key_actions:
            self.key_actions[symbol]()

    def print_handlers(self):
        print "keys to try:", \
            [symbol_string(k) for k in self.key_handlers.keys()]
        stdout.flush()

    def on_draw(self):
        """Clear the current OpenGL context, reset the model/view matrix and
        invoke the `draw()` methods of the zulus
        """
        self.camera.update()
        self.camera.focus(self.size_x, self.size_y)
        if not self.paused:
            self.gl_clear()
            zulus.render_all()
            # Make sure you tick the clock!
            pyglet.clock.tick()
            # Draw normal scene first, then switch to Orthomode and
            # draw the HUD as an overlay in this ortho-mode.
            self.camera.hud_mode(self.size_x, self.size_y)
            Land.display_fps.draw()
        pass

    def update(self,dt):
        if not self.paused:
            rules.tick_all(dt)
        pass

    def gl_setup(self):
        # Set the window color, this will be transparent in saved images.
        glClearColor(*bgcolor)
        # use glOrtho and turn off depthwriting and depthtesting
        glDisable(GL_DEPTH_TEST)
        glDepthMask(GL_FALSE)
        glClearColor(*self.bgcolor)
        glLoadIdentity() # reset transformation matrix
        # Most of this is already taken care of in Pyglet.
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        #glOrtho(0, self.width, 0, self.height, -1, 1)
        #glMatrixMode(GL_MODELVIEW)
        # Enable line anti-aliasing.
        glEnable(GL_LINE_SMOOTH)
        # Enable alpha transparency.
        glEnable(GL_BLEND)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def gl_clear(self):
        glClear(GL_COLOR_BUFFER_BIT)
        #glClear(GL_DEPTH_BUFFER_BIT)
        #glClear(GL_STENCIL_BUFFER_BIT)
        #glLoadIdentity()

    def toggle_pause(self):
        self.paused=(True,False)[self.paused]

    def get_display_size(self):
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        xmax = screen.width
        ymax = screen.height
        return(xmax,ymax)

    def image_capture(self,dt):
        global n
        n+=1
        file_num=str(n).zfill(5)
        filename="fr-"+file_num+'.png'
        pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
        if n>300: exit()

    def run(self):
        pyglet.app.run()
#--- FUNCTIONS ----------------------------------------------------------------




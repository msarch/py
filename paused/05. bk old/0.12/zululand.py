#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : main pyglet canvas, events and display loop

# bbw r12

##  IMPORTS -----------------------------------------------------------------

import pyglet
from pyglet.gl import *
from pyglet.window import key


##  CONSTANTS AND VARIABLES ---------------------------------------------------

##  CANVAS --------------------------------------------------------------------
class Zululand(pyglet.window.Window):

    def __init__(self):
        pyglet.window.Window.__init__(self,fullscreen=True)
        self.set_mouse_visible(False)
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        self.xmax = screen.width
        self.ymax = screen.height
        self.xc = (self.xmax*0.5)+1
        self.yc = (self.ymax*0.5)+1
        glClearColor(0.0, 0.0, 0.0, 0.0) # set background color to black
        #glClearColor(1.0, 1.0, 1.0, 1.0) # set background color to white
        glLoadIdentity() # reset transformation matrix
        glTranslatef(self.xc,self.yc,0.0)   # Move Origin to screen center
        self.frame=0
        self.elapsed=0
        self.zulus=[]

        # schedule the update function, 60 times per second
        pyglet.clock.schedule_interval(self.update, 1.0/60.0)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:exit()
        if symbol == key.SPACE:pause=not(pause)

    def on_mouse_press(self,x,y,button,modifiers):
        print x,y
        exit()

    def on_draw(self):
        """ Draws all elements of the canvas.
        """

        self.clear()
        for z in self.zulus:z.draw()

    def append(self,z):
        self.zulus.append(z)

    def remove(self, z):
        self.zulus.remove(z)

    def clear(self):
        """ Clears the previous frame from the canvas.
        """
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glClear(GL_STENCIL_BUFFER_BIT)

    def run(self, pause=None):
        """ Opens the application windows and starts drawing the canvas.
        """
        #TODO : implementer une pause avec 'space'; voir grease?
        pyglet.app.run()

    def update(self,dt):
        """ Updates the canvas zulus.
            This method does not actually draw anything, it only updates the state.
        """
        # Advance the animation by updating the tribe.
        self.frame += 1
        self.elapsed += dt
        for z in self.zulus:
            z.listen(dt)
            z.update(dt)
        for z in self.zulus:
            z.publish(dt)
        print self.frame
        print self.elapsed

    def render(self):
        """ Returns a screenshot of the current frame as a texture.
            This texture can be passed to the image() command.
        """
        return pyglet.image.get_buffer_manager().get_color_buffer().get_texture()

    def save(self, path):
        """ Exports the current frame as a PNG-file.
        """
        pyglet.image.get_buffer_manager().get_color_buffer().save(path)


##---CANVAS ELEMENTS -------------------------------------------
class Zulu(object):
    """ zulus inhabitants
        have 'emit', 'listen', 'update' and 'draw' methods
        those methods are called                                                                        """
    def __init__(self, **kwargs):
        pass

    def listen(self,dt, **kwargs):
        """ draw to screen.
        """
        pass

    def update(self, dt):
        """ draw to screen.
        """
        pass

    def publish(self,dt, **kwargs):
        """ draw to screen.
        """
        pass

    def draw(self, **kwargs):
        """ draw to screen.
        """
        pass


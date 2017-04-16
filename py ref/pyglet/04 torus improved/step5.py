#!/usr/bin/env python

"""
step5.py
-----------------
Step 5 of in_progress
a..removed the torus class
b..imported obj,py an obj file loader by Alex Holkner
c..called the obj loaders's draw method to draw the loaded cube
d..moved the glTranslatef(0, 0, -4) call to -3.. experiment with this value
e..added auto object rotation

Author
------
Jestermon 2009
jestermon.weebly.com
jestermonster@gmail.com
"""


import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
import os
import obj

from math import pi, sin, cos




##################################
class World(pyglet.window.Window):
    """This class inherits everything from pyglet.window.Window so that it
       can overload and use its own event handlers"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self):
        """Intitalize the class"""
        self.initColors()
        self.setWindow(600,400,"step5 ~ in progress",self.BLACK)
        self.setProperties()
        self.setup()
        self.loadModels()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def initColors(self):
        self.BLACK = (0,0,0,1)
        self.WHITE = (1,1,1,1)
        self.RED = (1,0,0,1)
        self.GREEN = (0,1,0,1)
        self.BLUE = (0,0,1,1)
        self.YELLOW = (1,1,0,1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setTitle(self,title):
        super(World, self).set_caption(title)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setWindow(self,width,height,title,bgcolor):
        # Try and create a window with multisampling (antialiasing)
        config = Config(sample_buffers=1, samples=4,
                        depth_size=16, double_buffer=True,)
        try:
            """Call the parent class"""
            super(World, self).__init__(resizable=True, config=config)
        except:
            # Fall back to no multisampling for old hardware
            super(World, self).__init__(resizable=True)
        self.width = width
        self.height = height
        self.setTitle(title)
        self.setLighting(0, self.vec(.5, .5, 1, 0), self.vec(.5, .5, 1, 1), self.vec(1, 1, 1, 1),True)
        self.setLighting(1, self.vec(1, 0, .5, 0), self.vec(.5, .5, .5, 1), self.vec(1, 1, 1, 1),True)
        pyglet.clock.schedule(self.update)
        r,g,b,a = bgcolor
        glClearColor(r,g,b,a)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setProperties(self):
        #self.batch = pyglet.graphics.Batch()
        #self.torus = Torus(1, 0.3, 50, 30, batch=self.batch)
        self.rx = 0
        self.ry = 0
        self.rz = 0
        self.xspeed = 0
        self.yspeed = 0
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setLighting(self, lightNo, position, specular, diffuse,on_off):
        glEnable(GL_LIGHTING)
        if lightNo == 0:
           light = GL_LIGHT0
        elif lightNo == 1:
           light = GL_LIGHT1
        elif lightNo == 2:
           light = GL_LIGHT2
        if on_off == True:
            glEnable(light)
            glLightfv(light, GL_POSITION, position)
            glLightfv(light, GL_SPECULAR, specular)
            glLightfv(light, GL_DIFFUSE, diffuse)
        else:
            glDisable(light)
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """setup the environment"""
    def setup(self):
        # One-time GL setup
        glColor3f(1, 0, 0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        # Uncomment this line for a wireframe view
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.vec(0.5, 0, 0.3, 1))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, self.vec(1, 1, 1, 1))
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """Define a simple function to create ctypes arrays of floats"""
    def vec(self,*args):
        return (GLfloat * len(args))(*args)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def loadModels(self):
        self.box = obj.OBJ("data/box2.obj")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_resize(self,width, height):
        """Override the default on_resize handler to create a 3D projection"""
        #IMPORTANT NOTE: class wont work without this method, NEVER leave it out
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., width / float(height), .1, 1000.)
        glMatrixMode(GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """Overload on_draw event handler"""
    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -3)
        glRotatef(self.rz, 0, 0, 1)
        glRotatef(self.ry, 0, 1, 0)
        glRotatef(self.rx, 1, 0, 0)
        self.box.draw()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update(self,dt):
        self.rx += dt * 1
        self.ry += dt * 80
        self.rz += dt * 30
        self.rx %= 360
        self.ry %= 360
        self.rz %= 360
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def run(self):
        pyglet.app.run()
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """overload on_key event handler"""
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """overload mouse event handler..
       use for mouse buttonds and mouse position"""
    def on_mouse_press(self,x, y, button, modifiers):
        pass
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """overload mouse motion event handler.."""
    def on_mouse_motion(self,x, y, dx, dy):
        pass


if __name__ == "__main__":
   world = World()
   world.run()
        

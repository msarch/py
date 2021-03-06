#!/usr/bin/env python

"""
step4.py
-----------------
Step 4 of in_progress
a..Moved lighting to its own method setLighting()
b..Added bgcolor to setWindow() parameters
c..Added some constants for color reference in method initColors()
d..Removed mouse rotation

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

from math import pi, sin, cos


##################################
class Torus(object):

    list = None
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, radius, inner_radius, slices, inner_slices,
                 batch, group=None):
        # Create the vertex and normal arrays.
        vertices = []
        normals = []

        u_step = 2 * pi / (slices - 1)
        v_step = 2 * pi / (inner_slices - 1)
        u = 0.
        for i in range(slices):
            cos_u = cos(u)
            sin_u = sin(u)
            v = 0.
            for j in range(inner_slices):
                cos_v = cos(v)
                sin_v = sin(v)

                d = (radius + inner_radius * cos_v)
                x = d * cos_u
                y = d * sin_u
                z = inner_radius * sin_v

                nx = cos_u * cos_v
                ny = sin_u * cos_v
                nz = sin_v

                vertices.extend([x, y, z])
                normals.extend([nx, ny, nz])
                v += v_step
            u += u_step

        # Create a list of triangle indices.
        indices = []
        for i in range(slices - 1):
            for j in range(inner_slices - 1):
                p = i * inner_slices + j
                indices.extend([p, p + inner_slices, p + inner_slices + 1])
                indices.extend([p, p + inner_slices + 1, p + 1])

        self.vertex_list = batch.add_indexed(len(vertices)//3,
                                             GL_TRIANGLES,
                                             group,
                                             indices,
                                             ('v3f/static', vertices),
                                             ('n3f/static', normals))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def delete(self):
        self.vertex_list.delete()


##################################
class World(pyglet.window.Window):
    """This class inherits everything from pyglet.window.Window so that it
       can overload and use its own event handlers"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self):
        """Intitalize the class"""
        self.initColors()
        self.setWindow(600,400,"step4 ~ in progress",self.BLACK)
        self.setProperties()
        self.setup()

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
        self.batch = pyglet.graphics.Batch()
        self.torus = Torus(1, 0.3, 50, 30, batch=self.batch)
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
        glTranslatef(0, 0, -4)
        glRotatef(self.rz, 0, 0, 1)
        glRotatef(self.ry, 0, 1, 0)
        glRotatef(self.rx, 1, 0, 0)
        self.batch.draw()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update(self,dt):
        pass
        
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
        

#!/usr/bin/env python
#lesson2.py

# See original source and C based tutorial at http://nehe.gamedev.net

# This code was created by Richard Campbell '99 (ported to Python/PyOpenGL by John Ferguson 2000)
#John Ferguson at hakuin@voicenet.com

#Code ported for use with pyglet by Jess Hill (Jestermon) 2009
#jestermon.weebly.com
#jestermonster@gmail.com


#because these lessons sometimes need  openGL GLUT, you need to install
#pyonlgl as well as pyglet, in order for this sample them to work
#pyopengl ~ http://pyopengl.sourceforge.net
#pyglet   ~ http://www.pyglet.org


import pyglet
from pyglet.gl import *
from pyglet.window import key
from OpenGL.GLUT import * #<<<==Needed for GLUT calls


##################################World
class World(pyglet.window.Window):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self):
        config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
        try:
            super(World, self).__init__(resizable=True, config=config)
        except:
            super(World, self).__init__(resizable=True)
        self.setup()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setup(self):
        self.width = 640
        self.height = 480
        self.InitGL(self.width, self.height)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_draw(self):
        self.DrawGLScene()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_resize(self,w,h):
        self.ReSizeGLScene(w,h)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # A general OpenGL initialization function.  Sets all of the initial parameters.
    def InitGL(self,Width, Height):				# We call this right after our OpenGL window is created.
        glClearColor(0.0, 0.0, 0.0, 0.0)	   # This Will Clear The Background Color To Black
        glClearDepth(1.0)					      # Enables Clearing Of The Depth Buffer
        glDepthFunc(GL_LESS)				      # The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)			    	# Enables Depth Testing
        glShadeModel(GL_SMOOTH)			   	# Enables Smooth Color Shading
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()					      # Reset The Projection Matrix
   	 									            # Calculate The Aspect Ratio Of The Window
        #(pyglet initializes the screen so we ignore this call)
        #gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
    def ReSizeGLScene(self,Width, Height):
        if Height == 0:						      # Prevent A Divide By Zero If The Window Is Too Small
     	      Height = 1
        glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # The main drawing function.
    def DrawGLScene(self):
	     # Clear The Screen And The Depth Buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()					# Reset The View

        # Move Left 1.5 units and into the screen 6.0 units.
        glTranslatef(-1.5, 0.0, -6.0)

        # Draw a triangle
        glBegin(GL_POLYGON)                 # Start drawing a polygon
        glVertex3f(0.0, 1.0, 0.0)           # Top
        glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
        glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
        glEnd()                             # We are done with the polygon

        # Move Right 3.0 units.
        glTranslatef(3.0, 0.0, 0.0)

        # Draw a square (quadrilateral)
        glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
        glVertex3f(-1.0, 1.0, 0.0)          # Top Left
        glVertex3f(1.0, 1.0, 0.0)           # Top Right
        glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
        glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
        glEnd()                             # We are done with the polygon

        #  since this is double buffered, swap the buffers to display what just got drawn.
        #(pyglet provides the swap, so we dont use the swap here)
        #glutSwapBuffers()
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #(function included here for reference, we use the pyglet on_key_press instead)
    # The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
    def keyPressed(*args):
     	   # If escape is pressed, kill everything.
         if args[0] == ESCAPE:
   	       glutDestroyWindow(window)
   	       sys.exit()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #(the original main function..We dont use it, pyglet does all for us...here only fore reference)
    #(see self.setup() method for settting our screen size)
    def main():
   	global window
   	# For now we just pass glutInit one empty argument. I wasn't sure what should or could be passed in (tuple, list, ...)
   	# Once I find out the right stuff based on reading the PyOpenGL source, I'll address this.
   	glutInit(())
   	# Select type of Display mode:
   	#  Double buffer
   	#  RGBA color
   	# Alpha components supported
   	# Depth buffer
   	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
   	# get a 640 x 480 window
   	glutInitWindowSize(640, 480)
   	# the window starts at the upper left corner of the screen
   	glutInitWindowPosition(0, 0)
   	# Okay, like the C version we retain the window id to use when closing, but for those of you new
   	# to Python (like myself), remember this assignment would make the variable local and not global
   	# if it weren't for the global declaration at the start of main.
   	window = glutCreateWindow("Jeff Molofee's GL Code Tutorial ... NeHe '99")
      # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
   	# set the function pointer and invoke a function to actually register the callback, otherwise it
   	# would be very much like the C version of the code.
   	glutDisplayFunc (DrawGLScene)   #we do a call from the self.on_draw() method
   	# Uncomment this line to get full screen.
   	#glutFullScreen()
   	# When we are doing nothing, redraw the scene.
   	glutIdleFunc(DrawGLScene)
   	# Register the function called when our window is resized.
   	glutReshapeFunc (ReSizeGLScene)   #we do a call from the
   	# Register the function called when the keyboard is pressed.
   	glutKeyboardFunc (keyPressed)
   	# Initialize our window.
   	InitGL(640, 480)
   	# Start Event Processing Engine
   	glutMainLoop()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')


##################################main
if __name__ == "__main__":
    window = World()
    pyglet.app.run()







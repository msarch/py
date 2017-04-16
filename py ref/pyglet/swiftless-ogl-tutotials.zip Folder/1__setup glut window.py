#!/usr/bin/env python

"""
Lesson:
How to setup a Window with GLUT

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/window.html

Notes:
None for this file

Dependencies:
python:  hrrp://www.python.org
Pyglet:  http://www.pyglet.org


Converted to pyglet in September 2009 by :
Jestermon
jestermon.weebly.com
jestermonster@gmail.com
"""

import pyglet
from pyglet.gl import *
from OpenGL.GLUT import *



def display ():
    glClearColor (0.0,0.0,0.0,1.0)     #clear the color of the window
    glClear (GL_COLOR_BUFFER_BIT)      #clear teh Color Buffer (more buffers later on)
    glLoadIdentity()                   #load the Identity Matrix
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) #set the view
    glFlush()                          #flush it all to the screen


glutInit()
glutInitDisplayMode (GLUT_SINGLE)      #set up a basic display buffer (only singular for now)
glutInitWindowSize (500, 500)          #set whe width and height of the window
glutInitWindowPosition (100, 100)      #set the position of the window
glutCreateWindow ("A basic OpenGL Window") #set the caption for the window
glutDisplayFunc (display)            #call the display function to draw our world
glutMainLoop ()                      #initialize the OpenGL loop cycle


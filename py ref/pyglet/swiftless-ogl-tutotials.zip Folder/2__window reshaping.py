#!/usr/bin/env python

"""
Lesson:
Reshaping the Window in OpenGL 

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/window_reshaping.html

Notes:
(GLfloat) typecasts were removed
retained 'main' as a python function to keep the structured look of the C source

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


def cube ():
    glutWireCube(2)


def display ():
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    cube()
    glFlush()


def reshape (w, h): 
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)              #set it so we can play with the 'camera'
    glLoadIdentity ()                         #replace the current matrix with the Identity Matrix
    gluPerspective (60, w / h, 1.0, 100.0)    #set the angle of view, the ratio of sight, the near and far factors
    glMatrixMode (GL_MODELVIEW)               #switch back the the model editing mode.


def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_SINGLE)
    glutInitWindowSize (500, 500)       #set the size of the window
    glutInitWindowPosition (100, 100)   #/set the position of the window
    glutCreateWindow ("A basic OpenGL Window")
    glutDisplayFunc (display)
    glutReshapeFunc (reshape)
    glutMainLoop ()
    

main()

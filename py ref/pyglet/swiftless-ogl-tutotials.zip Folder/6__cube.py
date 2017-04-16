#!/usr/bin/env python

"""
Lesson:
How to draw a cube using GLUT

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/cube.html

Notes:
none for this file

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
import sys


def cube ():
    glColor3f(1.0, 0.0, 0.0)   #color the cube red
    glutWireCube(2)            #draw a wired cube with side lengths of 2


def display ():
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    cube()
    glFlush()


def reshape (w, h):
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective (60, w / h, 1.0, 100.0)
    glMatrixMode (GL_MODELVIEW)


def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_SINGLE)
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window")
    glutDisplayFunc (display)
    glutReshapeFunc (reshape)
    glutMainLoop ()


main()


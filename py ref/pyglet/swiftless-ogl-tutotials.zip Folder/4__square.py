#!/usr/bin/env python

"""
Lesson:
Creating a Square using the OpenGL API

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/square.html

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



def square ():
    glBegin(GL_QUADS)               #begin the four sided shape
    glVertex3f(-0.5, -0.5, 0.0)     #first corner at -0.5, -0.5
    glVertex3f(-0.5, 0.5, 0.0)      #second corner at -0.5, 0.5
    glVertex3f(0.5, 0.5, 0.0)       #third corner at 0.5, 0.5
    glVertex3f(0.5, -0.5, 0.0)      #fourth corner at 0.5, -0.5
    glEnd()                         #end the shape we are currently working on


def display ():
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    square()
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

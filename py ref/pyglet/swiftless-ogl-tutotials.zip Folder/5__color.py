#!/usr/bin/env python

"""
Lesson:
How to add colour to an object in OpenGL 

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/color.html

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
    glColor3f(1.0, 0.0, 0.0)     #this will set the square to red.
    glBegin(GL_QUADS)
    glVertex3f(-0.5, -0.5, 0.0)
    glVertex3f(-0.5, 0.5, 0.0)
    glVertex3f(0.5, 0.5, 0.0)
    glVertex3f(0.5, -0.5, 0.0)
    glEnd()

    
def display ():
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glLoadIdentity();
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

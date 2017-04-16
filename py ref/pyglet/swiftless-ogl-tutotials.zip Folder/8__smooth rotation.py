#!/usr/bin/env python

"""
Lesson:
How to achieve Smooth Rotation using the OpenGL API

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/smooth_rotation.html

Notes:
substituted ++ with +=1
added 'global angle' 

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


angle = 0.0 #set the angle of rotation

def cube ():
    glRotatef(angle, 1.0, 0.0, 0.0) #rotate on the x axis
    glRotatef(angle, 0.0, 1.0, 0.0) #rotate on the y axis
    glRotatef(angle, 0.0, 0.0, 1.0) #rotate on the z axis
    glColor3f(1.0, 0.0, 0.0)
    glutWireCube(2)


def display ():
    global angle
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    cube()
    glutSwapBuffers()
    angle +=0.1


def reshape (w, h):
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective (60, w / h, 1.0, 100.0)
    glMatrixMode (GL_MODELVIEW)


def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_DOUBLE) #set up the double buffering
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window")
    glutDisplayFunc (display)
    glutIdleFunc (display)
    glutReshapeFunc (reshape)
    glutMainLoop ()


main()

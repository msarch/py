#!/usr/bin/env python

"""
Lesson:
How to Rotate a Cube with the OpenGL API

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/rotation.html

Notes:
substituted ++ with +=1
added 'global angle' 
change angle increment from 1 to 0.1 (fast machines just see a whirr)

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


angle = 0.0     #the rotation value

def cube ():
    glRotatef(angle, 1.0, 0.0, 0.0)  #rotate on the x axis
    glRotatef(angle, 0.0, 1.0, 0.0)  #rotate on the y axis
    glRotatef(angle, 0.0, 0.0, 1.0)  #rotate on the z axis
    glColor3f(1.0, 0.0, 0.0) 
    glutWireCube(2) 


def display ():
    global angle
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    cube()
    glFlush()
    angle +=0.1    #update the angle of rotation


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
    glutIdleFunc (display)   #change any idle values accordingly
    glutReshapeFunc (reshape)
    glutMainLoop ()
    

main()

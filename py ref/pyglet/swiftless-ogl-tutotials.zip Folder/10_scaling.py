#!/usr/bin/env python

"""
Lesson:
How to Scale Shapes with the OpenGL API 

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/scaling.html

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


angle = 0.0

def cube ():
    #scaled
    glScalef( 2.0, 0.5, 1.0 )  #twice as wide, half the height, same depth
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)
    glColor4f(1.0, 0.0, 0.0, 0.25) #25% visible
    glutWireCube(2)
    #non scaled
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)
    glColor4f(0.0, 1.0, 0.0, 0.25) #25% visible
    glutSolidCube(1)


def display ():
    global angle
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND); #enable the blending
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # set the blending
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
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGBA) #set up for the alpha channel
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window")
    glutDisplayFunc (display)
    glutIdleFunc (display)
    glutReshapeFunc (reshape)
    glutMainLoop ()
    

main()

#!/usr/bin/env python

"""
Lesson:
How to Pop and Push Matrices with the OpenGL API 

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/pop_and_push_matrices.html

Notes:
none


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
from pyglet import image
from OpenGL.GLUT import *
import sys


angle = 0.0    #angle for cube1
tangle = 0.0;  #angle for cube2

def cube ():
    glPushMatrix()                    #set where to start the current object transformations
    glTranslatef(1, 0, 0)             #move cube1 to the right
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)
    glColor3f(1.0, 0.0, 0.0)          #change cube1 to red
    glutWireCube(2)
    glPopMatrix()                     #end the current object transformations


def cube2 ():
    glPushMatrix()                    #set where to start the current object transformations
    glTranslatef(-1, 0, 0)            #move cube2 to the left
    glRotatef(tangle, 1.0, 0.0, 0.0)
    glRotatef(tangle, 0.0, 1.0, 0.0)
    glRotatef(tangle, 0.0, 0.0, 1.0)
    glColor3f(0.0, 1.0, 0.0)          #change cube2 to green
    glutWireCube(2)
    glPopMatrix()                     #end the current object transformations


def display ():
    global angle, tangle
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glLoadIdentity();
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    cube()
    cube2()
    glutSwapBuffers()
    angle+= 0.1
    tangle+= 0.2


def reshape (w, h):
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective (60, w / h, 1.0, 100.0)
    glMatrixMode (GL_MODELVIEW)


def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_DOUBLE)
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window")
    glutDisplayFunc (display)
    glutIdleFunc (display)
    glutReshapeFunc (reshape)
    glutMainLoop ()
    

main()


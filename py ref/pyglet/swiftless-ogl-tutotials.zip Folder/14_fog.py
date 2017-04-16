#!/usr/bin/env python

"""
Lesson:
How to use Fog in OpenGL

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/fog.html

Notes:
added required global definitions
added ESC to exit

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

def vec(self,*args):
    return (GLfloat * len(args))(*args)

density = 0.3  #set the density to 0.3 which is acctually quite thick
fogColor = vec(0.5, 0.5, 0.5, 1.0) #set the for color to grey

def cube ():
    global angle
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)
    glColor3f(1.0, 0.0, 0.0)
    glutSolidCube(2)


def init ():
    glEnable (GL_DEPTH_TEST)       #enable the depth testing
    glEnable (GL_FOG)              #enable the fog
    glFogi (GL_FOG_MODE, GL_EXP2)  #set the fog mode to GL_EXP2
    glFogfv (GL_FOG_COLOR, fogColor)  #set the fog color to our color chosen above
    glFogf (GL_FOG_DENSITY, density)  #set the density to the  value above
    glHint (GL_FOG_HINT, GL_NICEST)   #set the fog to look the nicest, may slow down on older cards


def display ():
    global angle
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    cube()
    glutSwapBuffers()
    angle += 0.1


def reshape (w, h):
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective (60, w / h, 1.0, 100.0)
    glMatrixMode (GL_MODELVIEW)


def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window")
    init ()
    glutDisplayFunc (display)
    glutIdleFunc (display)
    glutReshapeFunc (reshape)
    glutMainLoop ()
    

main()

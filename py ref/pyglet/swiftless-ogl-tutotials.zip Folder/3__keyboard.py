#!/usr/bin/env python

"""
Lesson:
How to use keyboard interactions with GLUT 

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/keyboard.html

Notes:
added 'ord()' to get key value

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


def display ():
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glFlush()


def keyboard (key, x, y):
    key = ord(key)
    if (key==27):        #27 is the ascii code for the ESC key
        sys.exit(0);     #end the program

def main(): 
    glutInit()
    glutInitDisplayMode (GLUT_SINGLE)
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window")
    glutDisplayFunc (display)
    glutKeyboardFunc (keyboard)   #the call for the keyboard function.
    glutMainLoop ();
    

main()

#!/usr/bin/env python

"""
Lesson:
How to setup Display Lists in OpenGL 

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/displaylists.html

Notes:
started removing redundant comments


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
from math import sin,cos


cubelist = None   #we are going to hold our list in here

#create the cube display list
def createcube ():
    global cubelist
    cubelist = glGenLists(1)         #set the cube list to Generate a List
    glNewList(cubelist,GL_COMPILE)   #compile the new list
    glPushMatrix()
    glutSolidCube(2)                 #draw the cube
    glPopMatrix() 
    glEndList()                      #end the list


def init ():
    glEnable (GL_DEPTH_TEST)  #enable the depth testing
    glEnable (GL_LIGHTING)    #enable the lighting
    glEnable (GL_LIGHT0)      #enable LIGHT0, our Diffuse Light
    glShadeModel (GL_SMOOTH)  #set the shader to smooth shader
    createcube()              #call the command to create the cube


def display ():
    global cubelist
    glClearColor (0.0,0.0,0.0,1.0);   #clear the screen to black
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); #clear the color buffer and the depth buffer
    glLoadIdentity()
    glTranslatef(0,0,-5)
    glCallList(cubelist)              #call the cube list
    glutSwapBuffers()                 


def reshape (w, h):
    glViewport (0, 0, w, h)                #set the viewport to the current window specifications
    glMatrixMode (GL_PROJECTION)           #set the matrix to projection
    glLoadIdentity ()
    gluPerspective (60, w / h, 1.0, 100.0) #set the perspective (angle of sight, width, height, , depth
    glMatrixMode (GL_MODELVIEW)            #set the matrix back to model


def keyboard (key, x, y):
    if ord(key)==27:
        glutLeaveGameMode()  #set the resolution how it was
        sys.exit(0)          #quit the program


def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_DEPTH); 
    glutGameModeString( "1024x768:32@75" )          
    glutEnterGameMode()                             
    init ()                                         
    glutDisplayFunc (display)                       
    glutIdleFunc (display); 
    glutReshapeFunc (reshape)                       
    glutKeyboardFunc (keyboard);                    
    glutMainLoop ()                                 
    

main()

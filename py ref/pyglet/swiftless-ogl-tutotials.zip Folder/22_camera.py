#!/usr/bin/env python

"""
Lesson:
Creating a basic camera for use in OpenGL

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/camera.html

Notes:
Converted fine, but the movement is not as anticipated
moved enable() call out of the display loop
Removed 'angle' variable from the program, since it is not used


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
import random



xpos = 0
ypos = 0
zpos = 0
xrot = 0
yrot = 0


#positions of the cubes
positionz = []
positionx = []


#set the positions of the cubes
#We could use tupples here, but let's not deviate from the original
def cubepositions ():
    global positionz, positionx
    for i in range(0,10):
        positionz.append(random.randint(0,5))
        positionx.append(random.randint(0,5))


#draw the cube
def cube ():
    global positionz, positionx
    for i in range(0,10):
        glPushMatrix()
        glTranslated(-positionx[i] * 10.0, 0, -positionz[i] *10.0)  #translate the cube
        glutSolidCube(2) # draw the cube
        glPopMatrix()


def init ():
    cubepositions()


def enable ():
    glEnable (GL_DEPTH_TEST)   #enable the depth testing
    glEnable (GL_LIGHTING)     #enable the lighting
    glEnable (GL_LIGHT0)       #enable LIGHT0, our Diffuse Light
    glShadeModel (GL_SMOOTH)   #set the shader to smooth shader


def camera ():
    global xpos, ypos, zpos, xrot, yrot
    glRotatef(xrot,1.0,0.0,0.0)      #rotate our camera on the x-axis (left and right)
    glRotatef(yrot,0.0,1.0,0.0)      #rotate our camera on the y-axis (up and down)
    glTranslated(-xpos,-ypos,-zpos)  #translate the screen to the position of our camera


def display ():
    glClearColor (0.0,0.0,0.0,1.0) 
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    camera()
    cube();
    glutSwapBuffers()
    

def reshape (w, h):
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective (60, w / h, 1.0, 1000.0)
    glMatrixMode (GL_MODELVIEW)


def keyboard (key, x, y):
    global xpos, ypos, zpos, xrot, yrot
    
    if (key=='q'):
        xrot += 1
        if (xrot >360):
            xrot -= 360

    if (key=='z'):
        xrot -= 1
        if (xrot < -360):
            xrot += 360

    if (key=='w'):
        yrotrad = (yrot / 180 * 3.141592654)
        xrotrad = (xrot / 180 * 3.141592654)
        xpos += float(sin(yrotrad)) 
        zpos -= float(cos(yrotrad)) 
        ypos -= float(sin(xrotrad)) 

    if (key=='s'):
        yrotrad = (yrot / 180 * 3.141592654)
        xrotrad = (xrot / 180 * 3.141592654)
        xpos -= float(sin(yrotrad))
        zpos += float(cos(yrotrad)) 
        ypos += float(sin(xrotrad))

    if (key=='d'):
        yrot += 1
        if (yrot >360):
            yrot -= 360

    if (key=='a'):
        yrot -= 1
        if (yrot < -360):
            yrot += 360

    if ord(key)==27:
        sys.exit(0)
        

def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window"); 
    init ()
    glutDisplayFunc (display)
    glutIdleFunc (display);
    glutReshapeFunc (reshape)
    glutKeyboardFunc (keyboard)
    enable()
    glutMainLoop ()
    

main()

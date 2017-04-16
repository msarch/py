#!/usr/bin/env python

"""
Lesson:
Creating a slightly more advanced camera for use in OpenGL

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/camera2.html

Notes:
By the time I got to this tutorial, I got bored...
but the conversions are straight forward, so you should easily follow the rest of Donald's tutorials

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
angle=0.0

lastx = 0
lasty = 0


positionz= []
positionx= []


def cubepositions ():
    global positionz, positionx
    for i in range(0,10):
        positionz.append(random.randint(0,5))
        positionx.append(random.randint(0,5))



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

    if (key=='s'):
        yrotrad = (yrot / 180 * 3.141592654)
        xrotrad = (xrot / 180 * 3.141592654)
        xpos -= float(sin(yrotrad))
        zpos += float(cos(yrotrad)) 
        ypos += float(sin(xrotrad))

    if (key=='d'):
        yrotrad = (yrot / 180 * 3.141592654)
        xpos += float(cos(yrotrad)) * 0.2
        zpos += float(sin(yrotrad)) * 0.2
    
    if (key=='a'):
        yrotrad = (yrot / 180 * 3.141592654)
        xpos -= float(cos(yrotrad)) * 0.2
        zpos -= float(sin(yrotrad)) * 0.2
        
    if ord(key)==27:
        sys.exit(0)
    

def mouseMovement(x, y):
    global lastx, lasty, xrot, yrot
    diffx=x-lastx      #check the difference between the current x and the last x position
    diffy=y-lasty      #check the difference between the current y and the last y position
    lastx=x                #set lastx to the current x position
    lasty=y                #set lasty to the current y position
    xrot += diffy  #set the xrot to xrot with the addition of the difference in the y position
    yrot += diffx  #set the xrot to yrot with the addition of the difference in the x position


def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window")
    init ()
    glutDisplayFunc (display)
    glutIdleFunc (display)
    glutReshapeFunc (reshape)
    glutPassiveMotionFunc(mouseMovement) #check for mouse movement
    glutKeyboardFunc (keyboard)
    enable()
    glutMainLoop ()
    

main()

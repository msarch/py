#!/usr/bin/env python

"""
Lesson:
How to work with the different lighting types in the OpenGL API

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/lighting_types.html

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


#angle of rotation
angle = 0.0

#diffuse light color variables
dlr = 1.0
dlg = 1.0
dlb = 1.0

#ambient light color variables
alr = 1.0
alg = 1.0
alb = 1.0

#light position variables
lx = 0.0
ly = 0.0
lz = 1.0
lw = 0.0

def vec(self,*args):
    return (GLfloat * len(args))(*args)

#draw the cube
def cube ():
    glRotatef(angle, 1.0, 0.0, 0.0) #rotate on the x axis
    glRotatef(angle, 0.0, 1.0, 0.0) #rotate on the y axis
    glRotatef(angle, 0.0, 0.0, 1.0) #rotate on the z axis
    glutSolidCube(2) #draw the cube


def init ():
    glEnable (GL_DEPTH_TEST) #enable the depth testing
    glEnable (GL_LIGHTING)   #enable the lighting
    glEnable (GL_LIGHT0)     #enable LIGHT0, our Diffuse Light
    glEnable (GL_LIGHT1)     #enable LIGHT1, our Ambient Light
    glShadeModel (GL_SMOOTH) #set the shader to smooth shader

def display ():
    global angle
    global lx,ly,lz,lw
    global dlr,dlg,dlb
    global alr,alg,alb
    glClearColor (0.0,0.0,0.0,1.0)                      #clear the screen to black
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #/clear the color buffer and the depth buffer
    glLoadIdentity()
    DiffuseLight = vec(dlr, dlg, dlb)                   #set DiffuseLight[] to the specified values
    AmbientLight = vec(alr, alg, alb)                   #set AmbientLight [] to the specified values
    glLightfv (GL_LIGHT0, GL_DIFFUSE, DiffuseLight)     #change the light accordingly
    glLightfv (GL_LIGHT1, GL_AMBIENT, AmbientLight)     #change the light accordingly
    LightPosition = vec(lx, ly, lz, lw)                #set the LightPosition to the specified values
    glLightfv (GL_LIGHT0, GL_POSITION, LightPosition)   #change the light accordingly
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) #camera position, x,y,z, looking at x,y,z, Up Positions of the camera
    cube()                                              #call the cube drawing function
    glutSwapBuffers()                                   #swap the buffers
    angle+=0.1                                          #increase the angle


def reshape (w, h):
    glViewport (0, 0, w, h)        #set the viewport to the current window specifications
    glMatrixMode (GL_PROJECTION)   #set the matrix to projection
    glLoadIdentity ()
    gluPerspective (60, w / h, 1.0, 100.0) #set the perspective (angle of sight, width, height, , depth)
    glMatrixMode (GL_MODELVIEW)    #set the matrix back to model
    

def keyboard (key, x, y):
    global lx,ly,lz,lw
    global alr,alg,alb
    global dlr,dlg,dlb
    
    if ord(key) == 27:
        sys.exit(0)
        
    if key=='r':
        dlr = 1.0 #change light to red
        dlg = 0.0
        dlb = 0.0
        
    if key=='g':
        dlr = 0.0 #change light to green
        dlg = 1.0
        dlb = 0.0
    
    if key=='b':
        dlr = 0.0 #change light to blue
        dlg = 0.0
        dlb = 1.0
    
    if key=='w':
        ly += 10.0 #move the light up
    
    if key=='s' :
        ly -= 10.0 #move the light down
    
    if key=='a':
        lx -= 10.0 #move the light left
    
    if key=='d':
        lx += 10.0 #move the light right
    

def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_DEPTH); #set the display to Double buffer, with depth
    glutInitWindowSize (500, 500)                   #set the window size
    glutInitWindowPosition (100, 100)               #set the position of the window
    glutCreateWindow ("A basic OpenGL Window")      #the caption of the window
    init ()                                         #call the init function
    glutDisplayFunc (display)                       #use the display function to draw everything
    glutIdleFunc (display)                          #update any variables in display, display can be changed to anyhing,
                                                    #as long as you move the variables to be updated, in this case, angle++;
    glutReshapeFunc (reshape)                       #reshape the window accordingly
    glutKeyboardFunc (keyboard)                     #check the keyboard
    glutMainLoop ()                                 #call the main loop
    

main()

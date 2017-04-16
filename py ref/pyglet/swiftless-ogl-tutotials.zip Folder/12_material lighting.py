#!/usr/bin/env python

"""
Lesson:
How to add Materials to Objects for Lighting within the OpenGL API 

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/material_lighting.html

Notes:
added vec function to convert lists to OGL floats (refer to pyglet source for this)

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


redDiffuseMaterial = vec(1.0, 0.0, 0.0)           #set the material to red
whiteSpecularMaterial = vec(1.0, 1.0, 1.0)        #set the material to white
greenEmissiveMaterial = vec(0.0, 1.0, 0.0)        #set the material to green
whiteSpecularLight = vec(1.0, 1.0, 1.0)           #set the light specular to white
blackAmbientLight = vec(0.0, 0.0, 0.0)            #set the light ambient to black
whiteDiffuseLight = vec(1.0, 1.0, 1.0)            #set the diffuse light to white
blankMaterial = vec(0.0, 0.0, 0.0)                #set the diffuse light to white
mShininess = vec(128)                             #set the shininess of the material

diffuse = False
emissive = False
specular = False


def init ():
    glEnable (GL_DEPTH_TEST)
    glEnable (GL_LIGHTING)
    glEnable (GL_LIGHT0)

def light ():
    glLightfv(GL_LIGHT0, GL_SPECULAR, whiteSpecularLight)
    glLightfv(GL_LIGHT0, GL_AMBIENT, blackAmbientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, whiteDiffuseLight)

def display ():
    global angle
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    light()
    glTranslatef(0,0,-5)
    glRotatef(angle,1,1,1)
    glutSolidTeapot(2)
    glutSwapBuffers()
    angle += 0.1
    

def reshape (w, h):
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective (60, w / h, 1.0, 100.0)
    glMatrixMode (GL_MODELVIEW)

def keyboard (key, x, y):
    global diffuse, emissive, specular
    if key=='s':
        if specular==False:
            specular = True
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, whiteSpecularMaterial)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mShininess)
        elif specular==True:
            specular = False
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, blankMaterial)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS,blankMaterial)
    
    if key=='d':
        if diffuse==False:
            diffuse = True
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE,redDiffuseMaterial)
        elif diffuse==True:
            diffuse = False
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, blankMaterial)
    
    if key=='e':
        if emissive==False:
            emissive = True
            glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION,greenEmissiveMaterial)
        elif emissive==True:
            emissive = False
            glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, blankMaterial)
    

def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window")
    init ()
    glutDisplayFunc (display)
    glutIdleFunc (display)
    glutKeyboardFunc (keyboard)
    glutReshapeFunc (reshape)
    glutMainLoop ()
    

main()

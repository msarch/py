#!/usr/bin/env python

"""
Lesson:
Was:    How to Texture your shapes on Windows
Is now: How to Texture your OGL shapes


Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/texture_under_windows.html

Notes:
This is the first sample to dviate from the original, since multiple platform support is
   intended by these code conversions..Refer to the link above, for original
Rwplaced the LoadTexture function with one that uses pyglet image library functions...
   this allows all pyglet supported image formats to be loaded, on all supported platforms
Used a cute kitten image from 'google'.. if someone owns it, shout, and i'll change it



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



texture = None #our global texture

angle = 0.0



def square ():
    global texture
    glBindTexture(texture.target, texture.id)
    glRotatef( angle, 1.0, 1.0, 1.0 ) 
    glBegin (GL_QUADS)
    glTexCoord2d(0.0,0.0); glVertex2d(-1.0,-1.0)  #with our vertices we have to assign a texcoord
    glTexCoord2d(1.0,0.0); glVertex2d(+1.0,-1.0)  #so that our texture has some points to draw to
    glTexCoord2d(1.0,1.0); glVertex2d(+1.0,+1.0)
    glTexCoord2d(0.0,1.0); glVertex2d(-1.0,+1.0)
    glEnd()


def LoadTexture(filename):
    global texture
    pic = image.load(filename)
    texture = pic.get_texture()
    width = pic.width
    height = pic.height
    rawimage = pic.get_image_data()
    format = 'RGBA'
    pitch = rawimage.width * len(format)
    pixels = rawimage.get_data(format, pitch)
    textures = c_uint()
    glGenTextures(1, byref(textures))
    glBindTexture(texture.target, texture.id)
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels);
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);


def display ():
    global angle
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glEnable( GL_TEXTURE_2D )
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    square()
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
    glutInitDisplayMode (GLUT_DOUBLE)
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window")
    glutDisplayFunc (display)
    glutIdleFunc (display)
    glutReshapeFunc (reshape)

    #Load our texture
    LoadTexture("kitten.bmp")

    glutMainLoop ()


main()

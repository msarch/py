#!/usr/bin/env python

"""
Lesson:
How to Enable Texture Coordinate Generation with the OpenGL API

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/texture_coordinate_generation.html

Notes: CONVERSION FAILURE 1
Used global texture variable, in keeping with the previous example.
...as the origional of this conversion of the code, is a rewrite by Donald anyway
After conversion, was surprised to see this this code is extremely slow under python
...then I was surprised to see that Donald placed the call ro LoadTexture inside the display loop
...Moved  the call out of the loop, and things worked at propper speed again
My little laptop seems to not work with the texture parameters as defined in the original...
..please refer to the original code to get all the info, and hopefully your OGL will do the job
..for now, I use LoadTexture(2) from the previous example, to provide some semblance of a working example


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


texture = None
angle = 0.0



def LoadTexture2(filename):
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
    
    glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE ) #set texture environment parameters

    #here we are setting what textures to use and when. The MIN filter is which quality to show
    #when the texture is near the view, and the MAG filter is which quality to show when the texture
    #is far from the view.

    #The qualities are (in order from worst to best)
    #GL_NEAREST
    #GL_LINEAR
    #GL_LINEAR_MIPMAP_NEAREST
    #GL_LINEAR_MIPMAP_LINEAR

    #And if you go and use extensions, you can use Anisotropic filtering textures which are of an
    #even better quality, but this will do for now.
    #glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR )
    #glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR_MIPMAP_LINEAR )
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);


    #Here we are setting the parameter to repeat the texture instead of clamping the texture
    #to the edge of our shape.
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )

    #Generate the texture with mipmaps
    gluBuild2DMipmaps( GL_TEXTURE_2D, 3, width, height, GL_RGB, GL_UNSIGNED_BYTE, pixels )



def cube ():
    global texture, angle
    glBindTexture(texture.target, texture.id)
    glRotatef( angle, 1.0, 1.0, 1.0 )
    glutSolidCube(2)


def display ():
    global angle, texture
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT)
    glLoadIdentity();
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glEnable( GL_TEXTURE_2D )  #enable 2D texturing
    glEnable(GL_TEXTURE_GEN_S) #enable texture coordinate generation
    glEnable(GL_TEXTURE_GEN_T)
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
    glutInitDisplayMode (GLUT_DOUBLE)
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("A basic OpenGL Window")
    glutDisplayFunc (display)
    glutIdleFunc (display)
    glutReshapeFunc (reshape)
    
    LoadTexture2( "kitten.bmp") #load the texture
    glutMainLoop ()
    

main()

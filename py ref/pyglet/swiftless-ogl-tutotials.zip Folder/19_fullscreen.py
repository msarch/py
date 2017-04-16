#!/usr/bin/env python

"""
Lesson:
How to set up a fullscreen window with GLUT 

Original Source for this lesson:
http://www.swiftless.com/tutorials/opengl/fullscreen.html

Notes:
variable 'angle' does nothing in this code, but I left it there

glut FullSceewn Mode:
glutGameModeString(Screen_Resolution:Color_Depth@Refresh_Rate)
examples: "800x600:24@70", "1024x768:32@75"


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


xpos = 0
ypos = 0
zpos = 0
xrot = 0
yrot = 90
angle=0.0


#draw the cubes, they make a fancy shape from above :P
def cube ():
    for i in range(0,50):
        glTranslated(1, 0, 1)
        glPushMatrix()
        glutSolidCube(2)  #draw the cube
        glPopMatrix()


def init ():
    glEnable (GL_DEPTH_TEST) #enable the depth testing
    glEnable (GL_LIGHTING)   #enable the lighting
    glEnable (GL_LIGHT0)     #enable LIGHT0, our Diffuse Light
    glShadeModel (GL_SMOOTH) #set the shader to smooth shader


def camera ():
    global xpos,ypos,zpos
    glRotatef(xrot,1.0,0.0,0.0)
    glRotatef(yrot,0.0,1.0,0.0)
    glTranslated(-xpos,-ypos,-zpos)


def display ():
    global angle
    glClearColor (0.0,0.0,0.0,1.0)   #clear the screen to black
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)   #clear the color buffer and the depth buffer
    glLoadIdentity()  
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) #camera position, x,y,z, looking at x,y,z, Up Positions of the camera
    camera()
    cube();             #call the cube drawing function
    glutSwapBuffers()   #swap the buffers
    angle+=1            #increase the angle


def reshape (w, h):
    glViewport (0, 0, w, h); #set the viewport to the current window specifications
    glMatrixMode (GL_PROJECTION) #set the matrix to projection
    glLoadIdentity ()
    gluPerspective (60, w / h, 1.0, 100.0) #set the perspective (angle of sight, width, height, , depth)
    glMatrixMode (GL_MODELVIEW)     #set the matrix back to model


def keyboard (key, x, y):
    global xpos, ypos, zpos, xrot, yrot
    if key=='q':
        xrot += 1
        if xrot >360:
            xrot -= 360
        
    if key=='z':
        xrot -= 1
        if xrot < -360:
            xrot += 360

    if key=='w':
        yrotrad = (yrot / 180 * 3.141592654)  #we could use math.pi here
        xrotrad = (xrot / 180 * 3.141592654)  #..but let's not change the code
        xpos += float(sin(yrotrad)) 
        zpos -= float(cos(yrotrad)) 
        ypos -= float(sin(xrotrad)) 

    if key=='s':
        yrotrad = (yrot / 180 * 3.141592654)
        xrotrad = (xrot / 180 * 3.141592654)
        xpos -= float(sin(yrotrad))
        zpos += float(cos(yrotrad)) 
        ypos += float(sin(xrotrad))

    if key=='d':
        yrot += 1
        if yrot >360:
            yrot -= 360

    if key=='a':
        yrot -= 1
        if yrot < -360:
            yrot += 360

    if ord(key)==27:
        glutLeaveGameMode() #set the resolution how it was
        sys.exit(0) #quit the program
    

def main ():
    glutInit ()
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_DEPTH)  #set the display to Double buffer, with depth
    glutGameModeString( "1024x768:32@75" )          #the settings for fullscreen mode
    glutEnterGameMode()                             #set glut to fullscreen using the settings in the line above
    init ()                                         #call the init function
    glutDisplayFunc (display)                       #use the display function to draw everything
    glutIdleFunc (display)                          #update any variables in display, display can be changed to
                                                    #..anyhing, as long as you move the variables to be updated,
                                                    #..in this case, angle++;
    glutReshapeFunc (reshape)                       #reshape the window accordingly
    glutKeyboardFunc (keyboard)                     #check the keyboard
    glutMainLoop ()                                 #call the main loop
    

main()

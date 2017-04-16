#!/usr/bin/env python
#lesson9.py

# See original source and C based tutorial at http://nehe.gamedev.net
#This code was created by Richard Campbell '99
#http://nehe.gamedev.net/lesson.asp?index=02

#This code was "created" by Jeff Molofee '99 (ported to
#Solaris/GLUT by Lakmal Gunasekara '99)
#(email Richard Campbell at ulmont@bellsouth.net)
#(email Lakmal Gunasekara at lakmal@gunasekara.de)

#Code ported for use with pyglet by Jess Hill (Jestermon) 2009
#jestermon.weebly.com
#jestermonster@gmail.com

#Because these lessons sometimes need  openGL GLUT, you need to install
#pyonlgl as well as pyglet, in order for some examples to work
#..note: if no glut routines are called, you can delete the opengl import line
#........this is a global comment template, and not revisited for each lesson

#May be required
#===============
#pyopengl ~ http://pyopengl.sourceforge.net

#Required
#========
#pyglet   ~ http://www.pyglet.org

import pyglet
from pyglet.gl import *
from pyglet import image #<==for image calls
from pyglet.window import key #<==for key constants
from OpenGL.GLUT import * #<==Needed for GLUT calls

#for this lesson
import time,struct,sys,random


##################################star
class Star:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self):
        self.r, self.g, self.b = (0, 0, 0)    # stars' color
        self.dist = 0.0                       # stars' distance from center
        self.angle = 0.0                      # stars' current angle


##################################star
class Image:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = None
        self.texture = None
    

##################################World
class World(pyglet.window.Window):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self):
        config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
        try:
            super(World, self).__init__(resizable=True, config=config)
        except:
            super(World, self).__init__(resizable=True)
        self.setup()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setup(self):
        self.width = 640
        self.height = 480
        self.globals()
        self.InitGL(self.width, self.height)
        pyglet.clock.schedule_interval(self.update, 1/60.0) # update at 60Hz


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """All globally defined variables placed here"""
    def globals(self):
        self.STAR_NUM = 50
        self.twinkle = 0
        self.stars = []
        for x in range(self.STAR_NUM):
	        self.stars.append(Star())
        self.zoom = -15.0   # viewing distance from stars.
        self.tilt = 90.0    # tilt the view
        self.spin = 0       # spin twinkling stars
        self.texture = range(1)
        self.myimage = Image()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ImageLoad(self,filename):
        pic = image.load(filename)
        texture = pic.get_texture()
        x = pic.width
        y = pic.height
        rawimage = pic.get_image_data()
        format = 'RGBA'
        pitch = rawimage.width * len(format)
        imagedata = rawimage.get_data(format, pitch)
        self.myimage.x = x
        self.myimage.y = y
        self.myimage.texture = texture
        self.myimage.image = imagedata

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def LoadGLTextures(self):
        self.ImageLoad("Data/Star.bmp")
        textures = c_uint()
        self.texture = glGenTextures(3, byref(textures))
        # linear filtered texture
        glBindTexture(self.myimage.texture.target, self.myimage.texture.id);   # 2d texture (x and y size)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR); # scale linearly when image bigger than texture
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR); # scale linearly when image smalled than texture
        glTexImage2D(GL_TEXTURE_2D, 0, 4, self.myimage.x, self.myimage.x, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.myimage.image);

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def InitGL(self,Width, Height):			              # We call this right after our OpenGL window is created.
        self.LoadGLTextures();                        # load the textures.
        glEnable(GL_TEXTURE_2D)                       # Enable texture mapping.
        glClearColor(0.0, 0.0, 0.0, 0.0)		      # This Will Clear The Background Color To Black
        glClearDepth(1.0)				              # Enables Clearing Of The Depth Buffer
        glShadeModel(GL_SMOOTH)			              # Enables Smooth Color Shading
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()				              # Reset The Projection Matrix
        gluPerspective(45.0,Width/Height,0.1,100.0)	  # Calculate The Aspect Ratio Of The Window
        glMatrixMode(GL_MODELVIEW)
        # setup blending
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)	          # Set The Blending Function For Translucency
        glEnable(GL_BLEND)                            # Enable Blending
        # set up the stars
        for loop in range(self.STAR_NUM):
        	self.stars[loop].angle = 0.0                       # initially no rotation.
        	self.stars[loop].dist = loop * 1.0 / self.STAR_NUM * 5.0         # calculate distance form the center
        	self.stars[loop].r = random.randrange(1, 256, 1)            # random red intensity;
        	self.stars[loop].g = random.randrange(1, 256, 1)            # random green intensity;
        	self.stars[loop].b = random.randrange(1, 256, 1)            # random blue intensity;

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ReSizeGLScene(self,Width, Height):
        if (Height==0):				# Prevent A Divide By Zero If The Window Is Too Small
    	    Height=1
        glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0,float(Width)/float(Height),0.1,100.0)
        glMatrixMode(GL_MODELVIEW)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def DrawGLScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)		# Clear The Screen And The Depth Buffer
        glBindTexture(self.myimage.texture.target, self.myimage.texture.id)     # pick the texture.
        for loop in range(self.STAR_NUM):        # loop through all the stars.
            glLoadIdentity()                        # reset the view before we draw each star.
            glTranslatef(0.0, 0.0, self.zoom)          # zoom into the screen.
            glRotatef(self.tilt, 1.0, 0.0, 0.0)       # tilt the view.
            glRotatef(self.stars[loop].angle, 0.0, 1.0, 0.0) # rotate to the current star's angle.
            glTranslatef(self.stars[loop].dist, 0.0, 0.0) # move forward on the X plane (the star's x plane).
            glRotatef(-self.stars[loop].angle, 0.0, 1.0, 0.0) # cancel the current star's angle.
            glRotatef(-self.tilt, 1.0, 0.0, 0.0)      # cancel the screen tilt.

            if (self.twinkle):                           # twinkling stars enabled ... draw an additional star.
                # assign a color using bytes
                glColor4ub(self.stars[self.STAR_NUM - loop-1].r, self.stars[self.STAR_NUM - loop-1].g, self.stars[self.STAR_NUM - loop-1].b, 255)
                glBegin(GL_QUADS)                  # begin drawing the textured quad.
                glTexCoord2f(0.0, 0.0)
                glVertex3f(-1.0, -1.0, 0.0)
                glTexCoord2f(1.0, 0.0)
                glVertex3f( 1.0, -1.0, 0.0)
                glTexCoord2f(1.0, 1.0)
                glVertex3f( 1.0,  1.0, 0.0)
                glTexCoord2f(0.0, 1.0)
                glVertex3f(-1.0, 1.0, 0.0)
                glEnd()                             # done drawing the textured quad.

            # main star
            glRotatef(self.spin, 0.0, 0.0, 1.0)       # rotate the star on the z axis.
            # Assign A Color Using Bytes
            glColor4ub(self.stars[loop].r,self.stars[loop].g,self.stars[loop].b,255)
            glBegin(GL_QUADS)			# Begin Drawing The Textured Quad
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-1.0,-1.0, 0.0)
            glTexCoord2f(1.0, 0.0)
            glVertex3f( 1.0,-1.0, 0.0)
            glTexCoord2f(1.0, 1.0)
            glVertex3f( 1.0, 1.0, 0.0)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-1.0, 1.0, 0.0)
            glEnd()				# Done Drawing The Textured Quad
            self.spin +=0.01                           # used to spin the stars.
            self.stars[loop].angle += loop * 1.0 / self.STAR_NUM * 1.0    # change star angle.
            self.stars[loop].dist  -= 0.01              # bring back to center.

            if (self.stars[loop].dist<0.0):             # star hit the center
                self.stars[loop].dist += 5.0            # move 5 units from the center.
                self.stars[loop].r = random.randrange(1, 256, 1)        # new red color.
                self.stars[loop].g = random.randrange(1, 256, 1)        # new green color.
                self.stars[loop].b = random.randrange(1, 256, 1)        # new blue color.



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update(self,dt):
        self.DrawGLScene()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_draw(self):
        self.DrawGLScene()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_resize(self,w,h):
        self.ReSizeGLScene(w,h)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def vec(self,*args):
        #creates a c_types vector
        return (GLfloat * len(args))(*args)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')
        elif symbol == key.T:
            if self.twinkle:		# switch the current value of twinkle, between 0 and 1.
                self.twinkle = 0
            else:
                self.twinkle = 1
        elif symbol == key.PAGEDOWN:
             self.zoom -= 0.2
        elif symbol == key.PAGEUP:
             self.zoom += 0.2
        elif symbol == key.UP:
             self.tilt -= 0.5
        elif symbol == key.DOWN:
             self.tilt += 0.5
             


##################################main
if __name__ == "__main__":
    window = World()
    pyglet.app.run()







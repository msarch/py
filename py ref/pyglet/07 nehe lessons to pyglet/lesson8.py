#!/usr/bin/env python
#lesson8.py

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
import time,struct,sys


##################################Image
class Image:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self,x,y,imagedata,texturedata):
        self.x = x
        self.y = y
        self.imagedata = imagedata
        self.texturedata = texturedata

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
        self.light = 0
        self.xrot = 0  
        self.yrot = 0  
        self.xspeed = 0
        self.yspeed = 0
        self.z = -5.0
        self.LightAmbient = self.vec(0.5, 0.5, 0.5, 1.0)
        self.LightDiffuse = self.vec(1.0, 1.0, 1.0, 1.0)
        self.LightPosition = self.vec(0.0, 0.0, 2.0, 1.0 )
        self.filter = 0	
        self.texture = range(3)
        self.blend = 0

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ImageLoad(self,filename):
        pic = pyglet.image.load(filename)
        texture = pic.get_texture()
        ix = pic.width
        iy = pic.height
        rawimage = pic.get_image_data()
        format = 'RGBA'
        pitch = rawimage.width * len(format)
        imagedata = rawimage.get_data(format, pitch)
        return Image(ix,iy,imagedata,texture)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def LoadGLTextures(self):
        self.myimage1 = self.ImageLoad("Data/glass.bmp")
        self.myimage2 = self.ImageLoad("Data/glass.bmp")
        self.myimage3 = self.ImageLoad("Data/glass.bmp")
        textures = c_uint()
        texture = glGenTextures(3, byref(textures))

        # texture 1 (poor quality scaling)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)  # cheap scaling when image bigger than texture
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)  # cheap scaling when image smalled than texture

        # 2d texture, level of detail 0 (normal), 3 components (red, green, blue), x size from image, y size from image,
        # border 0 (normal), rgb color data, unsigned byte data, and finally the data itself.
        glTexImage2D(GL_TEXTURE_2D, 0, 4, self.myimage1.x, self.myimage1.y, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.myimage1.imagedata)
        glBindTexture(self.myimage1.texturedata.target, self.myimage1.texturedata.id)   # 2d texture (x and y size)

        #due to limitations of my card, these seem not to work, any volunteers?
        # texture 2 (linear scaling)
        #glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)  # scale linearly when image bigger than texture
        #glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)  # scale linearly when image smalled than texture
        #glTexImage2D(GL_TEXTURE_2D, 0, 4, self.myimage2.x, self.myimage2.y, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.myimage2.imagedata);
        #glBindTexture(GL_TEXTURE_2D, self.myimage.texturedata.id)    # 2d texture (x and y size)

        # texture 3 (mipmapped scaling)
        #glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)  # scale linearly when image bigger than texture
        #glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)  # scale linearly + mipmap when image smalled than texture
        #glTexImage2D(GL_TEXTURE_2D, 0, 4, self.myimage3.x, self.myimage3.y, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.myimage3.imagedata)

        #2d texture, 3 colors, width, height, RGB in that order, byte data, and the data.
        #glTexImage2D(GL_TEXTURE_2D, 0, 4, self.myimage3.x, self.myimage3.y, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.myimage3.imagedata)
        #glBindTexture(self.myimage3.texturedata.target, self.myimage3.texturedata.id)    # 2d texture (x and y size)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def InitGL(self,Width, Height):	# We call this right after our OpenGL window is created.

        self.LoadGLTextures()                            # load the textures.
        glEnable(GL_TEXTURE_2D)                     # Enable texture mapping.

        glClearColor(0.0, 0.0, 0.0, 0.0)    	# This Will Clear The Background Color To Black
        glClearDepth(1.0)				# Enables Clearing Of The Depth Buffer
        glDepthFunc(GL_LESS)			# The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)			# Enables Depth Testing
        glShadeModel(GL_SMOOTH)			# Enables Smooth Color Shading

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()				# Reset The Projection Matrix

        gluPerspective(45.0,float(Width)/float(Height),0.1,100.0)	# Calculate The Aspect Ratio Of The Window

        glMatrixMode(GL_MODELVIEW)

        # set up light number 1.
        glLightfv(GL_LIGHT1, GL_AMBIENT, self.LightAmbient)  # add lighting. (ambient)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, self.LightDiffuse)  # add lighting. (diffuse).
        glLightfv(GL_LIGHT1, GL_POSITION,self.LightPosition) # set light position.
        glEnable(GL_LIGHT1)                             # turn light 1 on.

        # setup blending
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)			# Set The Blending Function For Translucency
        glColor4f(1.0, 1.0, 1.0, 0.5)

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
        glLoadIdentity()				# Reset The View
        glTranslatef(0.0,0.0,self.z)                     # move z units out from the screen.
        glRotatef(self.xrot,1.0,0.0,0.0)			# Rotate On The X Axis
        glRotatef(self.yrot,0.0,1.0,0.0)			# Rotate On The Y Axis
        glBindTexture(self.myimage1.texturedata.target, self.myimage1.texturedata.id)

        #glBindTexture(GL_TEXTURE_2D, self.texture[filter])   # choose the texture to use.
        glBegin(GL_QUADS)		                # begin drawing a cube

        # Front Face (note that the texture's corners have to match the quad's corners)
        glNormal3f( 0.0, 0.0, 1.0);     # front face points out of the screen on z.
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
        glTexCoord2f(1.0, 0.0)
        glVertex3f( 1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0)
        glVertex3f( 1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad
        # Back Face
        glNormal3f( 0.0, 0.0,-1.0)      # back face points into the screen on z.
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)	# Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0)
        glVertex3f( 1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
        glTexCoord2f(0.0, 0.0)
        glVertex3f( 1.0, -1.0, -1.0)	# Bottom Left Of The Texture and Quad
        # Top Face
        glNormal3f( 0.0, 1.0, 0.0)      # top face points up on y.
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0,  1.0,  1.0)	# Bottom Left Of The Texture and Quad
        glTexCoord2f(1.0, 0.0)
        glVertex3f( 1.0,  1.0,  1.0)	# Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0)
        glVertex3f( 1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
        # Bottom Face
        glNormal3f( 0.0, -1.0, 0.0)     # bottom face points down on y.
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0, -1.0, -1.0)	# Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0)
        glVertex3f( 1.0, -1.0, -1.0)	# Top Left Of The Texture and Quad
        glTexCoord2f(0.0, 0.0)
        glVertex3f( 1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
        # Right face
        glNormal3f( 1.0, 0.0, 0.0)      # right face points right on x.
        glTexCoord2f(1.0, 0.0)
        glVertex3f( 1.0, -1.0, -1.0)	# Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0)
        glVertex3f( 1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0)
        glVertex3f( 1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad
        glTexCoord2f(0.0, 0.0)
        glVertex3f( 1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
        # Left Face
        glNormal3f(-1.0, 0.0, 0.0)      # left face points left on x.
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)	# Bottom Left Of The Texture and Quad
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
        glEnd()                         # done with the polygon.
        self.xrot+=self.xspeed		    # X Axis Rotation
        self.yrot+=self.yspeed		    #  Y Axis Rotation


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
        elif symbol == key.L:
            if self.light == 0:
                self.light = 1
            else:
                self.light = 0      # switch the current value of light, between 0 and 1.
            if not self.light:
               glDisable(GL_LIGHTING);
            else:
               glEnable(GL_LIGHTING);
        elif symbol == key.F:
            self.filter+=1
            if self.filter>2:
                self.filter=0
        elif symbol == key.B:
            if self.blend == 0:		# switch the current value of blend, between 0 and 1.
                self.blend = 1
            else:
                self.blend = 0
            if not(self.blend):
               glDisable(GL_BLEND)              # Turn Blending Off
               glEnable(GL_DEPTH_TEST)          # Turn Depth Testing On
            else:
               glEnable(GL_BLEND)		         # Turn Blending On
               glDisable(GL_DEPTH_TEST)         # Turn Depth Testing Off
        elif symbol == key.PAGEUP:
             self.z-=0.02
        elif symbol == key.PAGEDOWN:
             self.z+=0.02
        elif symbol == key.UP:
            self.xspeed-=0.01
        elif symbol==key.DOWN:
            self.xspeed+=0.01
        elif symbol == key.LEFT:
            self.yspeed-=0.01
        elif symbol == key.RIGHT:
            self.yspeed+=0.01



##################################main
if __name__ == "__main__":
    window = World()
    pyglet.app.run()







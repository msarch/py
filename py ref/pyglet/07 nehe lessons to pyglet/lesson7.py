#!/usr/bin/env python
#lesson7.py

# See original source and C based tutorial at http://nehe.gamedev.net
#This code was created by Richard Campbell '99
#http://nehe.gamedev.net/lesson.asp?index=02

#This lesson ported from C, as there is no python vesion on the nene site
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
#May not be required
from OpenGL.GLUT import * #<==Needed for GLUT calls



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
        self.LoadGLTextures()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """All globally defined C variables will now be placed here"""
    def globals(self):
        self.light = True
        self.lp = False
        self.fp = True
        self.xrot = 0
        self.yrot = 0
        self.xspeed = 0
        self.yspeed = 0
        self.z = -5.0
        self.LightAmbient =	self.vec(0.5, 0.5, 0.5, 1.0)
        self.LightDiffuse =	self.vec(1.0, 1.0, 1.0, 1.0)
        self.LightPosition = self.vec(0.0, 0.0, 2.0, 1.0)
        self.filter = 0
        self.pgtexture = [] #list for textures
        self.pgimage = []   #list for images

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
    def loadImage(self,filename):
        pic = pyglet.image.load(filename)
        texture = pic.get_texture()
        ix = pic.width
        iy = pic.height
        rawimage = pic.get_image_data()
        format = 'RGBA'
        pitch = rawimage.width * len(format)
        myimage = rawimage.get_data(format, pitch)
        return (pic,texture,myimage)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def LoadGLTextures(self):
        #Was lazy here, perhaps this will be fixed some day :)
        pic1, mytexture1, myimage1 = self.loadImage("Data/Crate.bmp")
        pic2, mytexture2, myimage2 = self.loadImage("Data/Crate.bmp")
        pic3, mytexture3, myimage3 = self.loadImage("Data/Crate.bmp")
        self.pgtexture.append(mytexture1)
        self.pgtexture.append(mytexture2)
        self.pgtexture.append(mytexture3)
        self.pgimage.append(myimage1)
        self.pgimage.append(myimage2)
        self.pgimage.append(myimage3)

        #Create Three Textures
        textures = c_uint() #this is a c_types call, the way pyglet does things
        glGenTextures(3, byref(textures))

        # Create Nearest Filtered Texture
        glBindTexture(mytexture1.target, mytexture1.id)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, pic1.width, pic1.height, 0, GL_RGB, GL_UNSIGNED_BYTE, myimage1)

        # Create Linear Filtered Texture
        glBindTexture(mytexture2.target, mytexture2.id)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, pic2.width, pic2.height, 0, GL_RGB, GL_UNSIGNED_BYTE, myimage2)

        # Create MipMapped Texture
        glBindTexture(mytexture3.target, mytexture3.id)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 3,pic3.width, pic3.height, GL_RGB, GL_UNSIGNED_BYTE, myimage3)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def vec(self,*args):
        #creates a c_types vector
        return (GLfloat * len(args))(*args)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # A general OpenGL initialization function.  Sets all of the initial parameters.
    def InitGL(self,Width, Height):
        self.LoadGLTextures()
        glEnable(GL_TEXTURE_2D)
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.5)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glLightfv(GL_LIGHT1, GL_AMBIENT, self.LightAmbient)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, self.LightDiffuse)
        glLightfv(GL_LIGHT1, GL_POSITION, self.LightPosition)
        glEnable(GL_LIGHT1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ReSizeGLScene(self,Width, Height):
        if Height == 0:						     
              Height = 1
        glViewport(0, 0, Width, Height)		
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # The main drawing function.
    def DrawGLScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0,0.0,self.z)

        glRotatef(self.xrot,1.0,0.0,0.0)
        glRotatef(self.yrot,0.0,1.0,0.0)

        #This line is key, for swapping textures on a mesh...Jestermon
        glBindTexture(self.pgtexture[self.filter].target, self.pgtexture[self.filter].id)

        glBegin(GL_QUADS)
        #Front Face
        glNormal3f( 0.0, 0.0, 1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f( 1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        #Back Face
        glNormal3f( 0.0, 0.0,-1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f( 1.0, -1.0, -1.0)
        #Top Face
        glNormal3f( 0.0, 1.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        #Bottom Face
        glNormal3f( 0.0,-1.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f( 1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)
        #Right face
        glNormal3f( 1.0, 0.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f( 1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f( 1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f( 1.0, -1.0,  1.0)
        #Left Face
        glNormal3f(-1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glEnd()

        self.xrot+=self.xspeed;
        self.yrot+=self.yspeed;


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')
        if symbol == key.L:
            self.light = not self.light;
            if not self.light:
               glDisable(GL_LIGHTING);
            else:
               glEnable(GL_LIGHTING);
        if symbol == key.F:
            self.filter +=1
            if self.filter>2:
               self.filter=0
        if symbol == key.PAGEDOWN:
            self.z-=0.02
        if symbol == key.PAGEUP:
            self.z+=0.02
        if symbol == key.UP:
            self.xspeed-=0.01
        if symbol == key.DOWN:
            self.xspeed+=0.01
        if symbol == key.RIGHT:
            self.yspeed+=0.01
        if symbol == key.LEFT:
            self.yspeed-=0.01
            


##################################main
if __name__ == "__main__":
    window = World()
    pyglet.app.run()







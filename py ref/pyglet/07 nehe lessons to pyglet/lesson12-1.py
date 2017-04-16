#!/usr/bin/env python
#lesson12.py

"""
 *		This Code Was Created By bosco / Jeff Molofee 2000
 *		A HUGE Thanks To Fredric Echols For Cleaning Up
 *		And Optimizing The Base Code, Making It More Flexible!
"""

#Code ported for use with pyglet by Jess Hill (Jestermon) 2009
#jestermon.weebly.com
#jestermonster@gmail.com

#Because these lessons sometimes need  openGL GLUT, you need to install
#pyonlgl as well as pyglet, in order for some examples to work
#..note: if no glut routines are called, you can delete the opengl import line
#........this is a global comment template, and not revisited for each lesson

#for some reason this direct translation from C does not display anything,
#but I put it up for you to view the translated source anyway, perhaps a keen
#eye can pick up some flaw I missed :)

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


import time,struct,sys,random,math





##################################
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
        self.myimage = Image()
        self.box = 0
        self.top = 0
        self.xrot = 0
        self.yrot = 0
        self.boxcol = [self.vec(1.0,0.0,0.0),self.vec(1.0,0.5,0.0),self.vec(1.0,1.0,0.0),self.vec(0.0,1.0,0.0),self.vec(0.0,1.0,1.0)]
        self.topcol = [self.vec(0.5,0.0,0.0),self.vec(0.5,0.25,0.0),self.vec(0.5,0.5,0.0),self.vec(0.0,0.5,0.0),self.vec(0.0,0.5,0.5)]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def BuildLists(self):
    #Build Cube Display Lists
        self.box = glGenLists(2)				# Generate 2 Different Lists
        glNewList(self.box,GL_COMPILE)		# Start With The Box List
        glBegin(GL_QUADS)
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
        glEnd();
        glEndList();

        self.top = self.box + 1			#Storage For "Top" Is "Box" Plus One
        glNewList(self.top,GL_COMPILE)	#Now The "Top" Display List
        glBegin(GL_QUADS)
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
        glEnd();
        glEndList();
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def makeArray(self,n1,n2,n3,base):
        """python needs to build multidimentional arrays, which can be done in
        many ways, else the Numpy package my be used. Here we build it in
        reverse.. just to simlify a complex array, by using lists"""
        zz = [base]*n3              #zz= [0.0, 0.0, 0.0]
        yy = []
        for r in range(n2):        #yy= zz * n2
            yy.append(zz)
        xx = []
        for r in range(n1):        #xx= yy * n1
            xx.append(yy)
        return xx

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
        self.ImageLoad("Data/Cube.bmp")
        textures = c_uint()
        self.texture = glGenTextures(1, byref(textures))
        glBindTexture(self.myimage.texture.target, self.myimage.texture.id)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, self.myimage.x, self.myimage.x, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.myimage.image);
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def InitGL(self,Width, Height):
        self.LoadGLTextures()
    	self.BuildLists()								 #Jump To The Code That Creates Our Display Lists
    	glEnable(GL_TEXTURE_2D)							 #Enable Texture Mapping
    	glShadeModel(GL_SMOOTH)							 #Enable Smooth Shading
    	glClearColor(0.0, 0.0, 0.0, 0.5)				 #Black Background
    	glClearDepth(1.0)								 #Depth Buffer Setup
    	glEnable(GL_DEPTH_TEST)							 #Enables Depth Testing
    	glDepthFunc(GL_LEQUAL)							 #The Type Of Depth Testing To Do
    	glEnable(GL_LIGHT0)								 #Quick And Dirty Lighting (Assumes Light0 Is Set Up)
    	glEnable(GL_LIGHTING)							 #Enable Lighting
    	glEnable(GL_COLOR_MATERIAL)						 #Enable Material Coloring
    	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)#Really Nice Perspective Calculations

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def ReSizeGLScene(self,Width, Height):
        glViewport(0, 0, Width, Height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0,float(Width)/float(Height),0.1,100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def DrawGLScene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #Clear The Screen And The Depth Buffer
        glBindTexture(self.myimage.texture.target, self.myimage.texture.id)
        for yloop in range(6):
            for xloop in range(yloop):
                glLoadIdentity()
                glTranslatef(1.4+(float(xloop)*2.8)-(float(yloop)*1.4),((6.0-float(yloop))*2.4)-7.0,-20.0)
                glRotatef(45.0-(2.0*yloop)+self.xrot,1.0,0.0,0.0)
                glRotatef(45.0+self.yrot,0.0,1.0,0.0)
                glColor3fv(self.boxcol[yloop-1])
                glCallList(self.box)
                glColor3fv(self.topcol[yloop-1])
                glCallList(self.top)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update(self,dt):
        #self.DrawGLScene()
        pass

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
        elif symbol == key.LEFT:
            self.yrot-=0.2
        elif symbol == key.RIGHT:
            self.yrot+=0.2
        elif symbol == key.UP:
            self.xrot-=0.2
        elif symbol == key.DOWN:
            self.xrot+=0.2

            


##################################main
if __name__ == "__main__":
    window = World()
    pyglet.app.run()







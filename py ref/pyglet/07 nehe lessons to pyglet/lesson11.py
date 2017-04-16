#!/usr/bin/env python
#lesson11.py

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
        self.points = self.makeArray(45, 45, 3, 0.0)
        self.wiggle_count = 0
        self.xrot = 0
        self.yrot = 0
        self.zrot = 0
        self.hold = 0
        self.texture = None
        
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
        self.ImageLoad("Data/Tim.bmp")
        textures = c_uint()
        self.texture = glGenTextures(1, byref(textures))
        glBindTexture(self.myimage.texture.target, self.myimage.texture.id)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, self.myimage.x, self.myimage.x, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.myimage.image);
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def InitGL(self,Width, Height):
        self.LoadGLTextures()
    	glEnable(GL_TEXTURE_2D)
    	glShadeModel(GL_SMOOTH)
    	glClearColor(0.0, 0.0, 0.0, 0.5)
    	glClearDepth(1.0)
    	glEnable(GL_DEPTH_TEST)
    	glDepthFunc(GL_LEQUAL)
    	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    	glPolygonMode( GL_BACK, GL_FILL )
    	glPolygonMode( GL_FRONT, GL_LINE )

    	for x in range(45):
    		for y in range(45):
    			self.points[x][y][0]=float((x/5.0)-4.5)
    			self.points[x][y][1]=float((y/5.0)-4.5)
    			self.points[x][y][2]=float(math.sin((((x/5.0)*40.0)/360.0)*3.141592654*2.0))

        
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
    	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    	glLoadIdentity()
    	glTranslatef(0.0,0.0,-12.0)
    	glRotatef(self.xrot,1.0,0.0,0.0)
    	glRotatef(self.yrot,0.0,1.0,0.0)
    	glRotatef(self.zrot,0.0,0.0,1.0)
        glBindTexture(self.myimage.texture.target, self.myimage.texture.id)
    	glBegin(GL_QUADS)
    	for x in range(44):
    		for y in range(44):
    			float_x = float(x)/44.0
    			float_y = float(y)/44.0
    			float_xb = float(x+1)/44.0
    			float_yb = float(y+1)/44.0
    			glTexCoord2f( float_x, float_y);
    			glVertex3f( self.points[x][y][0], self.points[x][y][1], self.points[x][y][2] )
    			glTexCoord2f( float_x, float_yb )
    			glVertex3f( self.points[x][y+1][0], self.points[x][y+1][1], self.points[x][y+1][2] )
    			glTexCoord2f( float_xb, float_yb )
    			glVertex3f( self.points[x+1][y+1][0], self.points[x+1][y+1][1], self.points[x+1][y+1][2] )
    			glTexCoord2f( float_xb, float_y )
    			glVertex3f( self.points[x+1][y][0], self.points[x+1][y][1], self.points[x+1][y][2] )
    	glEnd()

    	if self.wiggle_count == 2:
    		for y in range(45):
    			hold=self.points[0][y][2]
    			for x in range(44):
    				self.points[x][y][2] = self.points[x+1][y][2]
    			self.points[44][y][2]=hold
    		self.wiggle_count = 0
    		
    	self.wiggle_count+=1
    	self.xrot+=0.3
    	self.yrot+=0.2
    	self.zrot+=0.4
	
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


##################################main
if __name__ == "__main__":
    window = World()
    pyglet.app.run()







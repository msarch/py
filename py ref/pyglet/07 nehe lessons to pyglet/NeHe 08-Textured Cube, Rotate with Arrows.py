#!/usr/bin/env python
# pyglet version of NeHe's OpenGL lesson08
# based on the pygame+PyOpenGL conversion by Paul Furber 2001 - m@verick.co.za
# Philip Bober 2007 pdbober@gmail.com

from pyglet.gl import *
from pyglet import window
from pyglet import image
from pyglet.window import key
import pyglet.clock
import os

xrot = yrot = 0.0
xspeed = yspeed = 0.0
z = -5.0
textures = []
filter = 0
light = False
blend = False

LightAmbient  = (GLfloat*4)(0.5, 0.5, 0.5, 1.0)
LightDiffuse  = (GLfloat*4)(1.0, 1.0, 1.0, 1.0)
LightPosition = (GLfloat*4)(0.0, 0.0, 2.0, 1.0)

def resize(width, height):
	if height==0:
		height=1
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, 1.0*width/height, 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

def init():
	glEnable(GL_TEXTURE_2D)
	load_textures()
	glShadeModel(GL_SMOOTH)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClearDepth(1.0)
	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	glLightfv( GL_LIGHT1, GL_AMBIENT, LightAmbient )
	glLightfv( GL_LIGHT1, GL_DIFFUSE, LightDiffuse )
	glLightfv( GL_LIGHT1, GL_POSITION, LightPosition )
	glEnable( GL_LIGHT1 )
	glColor4f( 1.0, 1.0, 1.0, 0.5)
	glBlendFunc( GL_SRC_ALPHA, GL_ONE )

def load_textures():
	global textures
	texturefile = os.path.join('data','glass.bmp')
	textureSurface = image.load(texturefile)

	t1=textureSurface.image_data.create_texture(image.Texture)
	glBindTexture(GL_TEXTURE_2D, t1.id)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	
	t2=textureSurface.image_data.create_texture(image.Texture)
	glBindTexture(GL_TEXTURE_2D, t2.id)
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )

	t3=textureSurface.mipmapped_texture
	glBindTexture( GL_TEXTURE_2D, t3.id)
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST )
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )

	textures=[t1,t2,t3]

def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(0.0, 0.0, z)

	glRotatef(xrot, 1.0, 0.0, 0.0)
	glRotatef(yrot, 0.0, 1.0, 0.0)
	
	glBindTexture(GL_TEXTURE_2D, textures[filter].id)
	
	glBegin(GL_QUADS)
	
	glNormal3f(0.0, 0.0, 1.0)
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad
	
	# Back Face
	glNormal3f(0.0, 0.0, -1.0)
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)	# Bottom Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)	# Bottom Left Of The Texture and Quad
	
	# Top Face
	glNormal3f(0.0, 1.0, 0.0)
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)	# Bottom Left Of The Texture and Quad
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)	# Bottom Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
	
	# Bottom Face
	glNormal3f(0.0, -1.0, 0.0)
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)	# Top Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)	# Top Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
	
	# Right face
	glNormal3f(1.0, 0.0, 0.0)
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)	# Bottom Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
	
	# Left Face
	glNormal3f(-1.0, 0.0, 0.0)
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)	# Bottom Left Of The Texture and Quad
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
	
	glEnd()
def on_key_press(sym, mod):
	global filter,light,xspeed,yspeed,z,blend
	if sym == key.ESCAPE:
		win.has_exit = True
	elif sym == key.F:
		filter = (filter + 1) % len(textures)
	elif sym == key.L:
		light = not light
		if not light:
			glDisable(GL_LIGHTING)
		else:
			glEnable(GL_LIGHTING)
	elif sym == key.B:
		blend = not blend
		if blend:
			glEnable(GL_BLEND)
			glDisable(GL_DEPTH_TEST)
		else:
			glEnable(GL_DEPTH_TEST)
			glDisable(GL_BLEND)
	elif sym == key.PAGEUP:
		z -= 0.05
	elif sym == key.PAGEDOWN:
		z += 0.05
	elif sym == key.UP:
		xspeed -= 5
	elif sym == key.DOWN:
		xspeed += 5
	elif sym == key.LEFT:
		yspeed -= 5
	elif sym == key.RIGHT:
		yspeed += 5
def main():
	global xrot,yrot,zrot,win
	win = window.Window(width=640,height=480,visible=False)
	win.on_resize=resize
	win.on_key_press=on_key_press

	init()

	win.set_visible()
	clock=pyglet.clock.Clock()

	while not win.has_exit:
		win.dispatch_events()
		
		draw()

		win.flip()

		dt=clock.tick()
		xrot += xspeed*dt
		yrot += yspeed*dt

	print "fps:  %d" % clock.get_fps()

if __name__ == '__main__': main()

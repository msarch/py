#!/usr/bin/env python
# pyglet version of NeHe's OpenGL lesson09
# based on the pygame+PyOpenGL conversion by Paul Furber 2001 - m@verick.co.za
# Philip Bober 2007 pdbober@gmail.com

from pyglet.gl import *
from pyglet import window
from pyglet import image
from pyglet.window import key
import pyglet.clock
import os,random


textures = []
stars = []
twinkle = 0
zoom = -15.0
tilt = 90.0
spin = 0.0

class Star:
	""" simple star class that (hopefully) demonstrates
	how to move functionality out of a main loop and into
	an object - the logic remains unchanged from the
	original tutorial C code"""
	def __init__(self, index, max=50):
		self.angle = 0.0
		self.index = index
		self.max = max
		self.dist = (1.0 * index/max) * 5.0
		self.r = random.randrange(0,256)
		self.g = random.randrange(0,256)
		self.b = random.randrange(0,256)

	def draw(self):
		glBegin( GL_QUADS )
		glTexCoord2f( 0.0, 0.0 ); glVertex3f( -1.0, -1.0, 0.0 )
		glTexCoord2f( 1.0, 0.0 ); glVertex3f(  1.0, -1.0, 0.0 )
		glTexCoord2f( 1.0, 1.0 ); glVertex3f(  1.0,  1.0, 0.0 )
		glTexCoord2f( 0.0, 1.0 ); glVertex3f( -1.0,  1.0, 0.0 )
		glEnd( )

	def set_color(self):
		glColor4ub(self.r, self.g, self.b, 255)

	def orient(self):
		global zoom, tilt, twinkle, stars
		glLoadIdentity( )
		glTranslatef( 0.0, 0.0, zoom )
		glRotatef( tilt, 1.0, 0.0, 0.0 )
		glRotatef( self.angle, 0.0, 1.0, 0.0 )
		glTranslatef( self.dist, 0.0, 0.0 )
		glRotatef( -self.angle, 0.0, 1.0, 0.0 )
		glRotatef( -tilt, 1.0, 0.0, 0.0 )
		if twinkle:
			self.r = stars[self.max - self.index - 1].r
			self.g = stars[self.max - self.index - 1].g
			self.b = stars[self.max - self.index - 1].b
			self.set_color()
			self.draw()
		glRotatef( spin, 0.0, 0.0, 1.0 )
 
	def update(self):
		global spin
		self.orient()
		self.set_color()
		self.draw()
		spin += 0.01
		self.angle += 1.0*self.index / self.max
		self.dist -= 0.01
		if ( self.dist < 0.0 ):
			self.dist += 5.0
			self.r = random.randrange(0,256)
			self.g = random.randrange(0,256)
			self.b = random.randrange(0,256)

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
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	glBlendFunc( GL_SRC_ALPHA, GL_ONE )
	glEnable(GL_BLEND)
	for x in range(50):
		stars.append(Star(x))
def load_textures():
	global texture
	textureSurface = image.load('star.bmp')
	texture=textureSurface.texture
	glBindTexture(GL_TEXTURE_2D, texture.id)
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )

def draw():
	glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glBindTexture( GL_TEXTURE_2D, texture.id )

	glLoadIdentity( )

	for star in stars:
		star.update()
def on_key_press(sym, mod):
	global tilt, zoom, twinkle
	if sym == key.ESCAPE:
		win.has_exit = True
	elif sym == key.UP:
		tilt += 2.0
	elif sym == key.DOWN:
		tilt -= 2.0
	elif sym == key.PAGEUP:
		zoom += 0.5
	elif sym == key.PAGEDOWN:
		zoom -=0.5
	elif sym == key.T:
		twinkle = not twinkle

def main():
	global win
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
	print "fps:  %d" % clock.get_fps()

if __name__ == '__main__': main()

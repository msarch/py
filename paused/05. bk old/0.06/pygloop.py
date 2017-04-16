#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : main pyglet loop

# r0.6

##--- IMPORTS ------------------------------------------------------------------------------
import pyglet
from pyglet import clock
from pyglet.gl import *
from pyglet import window
from pyglet.window import key
import scenario

##--- CONSTANTS ----------------------------------------------------------------------------
frames_tick=1.0/25.0 # pas de division d'int dont le resultat serait 0 !!!
sound_tick=5
sound1 = pyglet.resource.media('tt.wav', streaming=False)

##--- CANVAS --------------------------------------------------------------------------------

class Canvas(pyglet.window.Window):

	def __init__(self):

		window.Window.__init__(self,fullscreen=True)

		glShadeModel(GL_SMOOTH)	# Enables smooth shading
		glClearColor(0.0, 0.0, 0.0, 0.0) # set background color to black
		glLoadIdentity() # reset transformation matrix
		# glClearDepth(1.0)		# Depth buffer setup
		# glEnable(GL_DEPTH_TEST)		# Enables depth testing
		# glDepthFunc(GL_LEQUAL)		# The type of depth test to do
		# glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)	# Really nice perspective calculations

		# Initialize screen resolution
		platform = pyglet.window.get_platform()
		display = platform.get_default_display()
		screen = display.get_default_screen()
		self.screen_width = screen.width
		self.screen_height = screen.height

	def on_key_press(self, symbol, modifiers):
			sound1.play()
			if symbol == key.ESCAPE:
				exit()

	def on_mouse_press(self,x,y,button,modifiers):
		pass

	def draw(self,dt):

		glClear(GL_COLOR_BUFFER_BIT |GL_DEPTH_BUFFER_BIT)
		glColor3f(0.5, 0.5, 1.0)	# set the color to sky-blue
		# pyglet.gl.glColor4f(0.23,0.23,0.23,1.0) # gray
		scenario.geom_draw() # get all the drawing
		scenario.geom_update(dt)

		print 'FPS is %f' % clock.get_fps()

		return pyglet.event.EVENT_HANDLED

	def timed_sound(self,dt):
		sound1.play()

##--- MAIN ----------------------------------------------------------------------------------------

def main():
	c = Canvas()
	scenario.geom_init()
	clock.schedule_interval(c.draw, frames_tick)
	clock.schedule_interval(c.timed_sound, sound_tick)
	pyglet.app.run()

##-------------------------------------------------------------------------------------------

if __name__ == "__main__": main()

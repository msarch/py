#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : draws rectangles,

# r0.5

##--- COMMENTS ----------------------------------------------------------------------------------------
# - r0.1 :
#       - simples rectangles
# - r0.2 :
#       - layers et import des rect depuis fichier csv
#       - Refs:   - nodebox exemples, 01-drag.py)
# - r0.3 :
#       - plus de dépendence Nodebox => IS A PYGLET APP
#       - Refs:
#               - nodebox.graphics.geometry --> classes et operations sur geométrie 2d
#               - nodebox.graphics.context  --> gère l'interface avec pyglet
#                                           --> génère les commandes opengl pour rect, triangle, bezier, etc..
#               - pyglet doc
#       - pour l'instant, affiche une liste de géométrie,
# - r0.4 :
#		- utilisation de l'event loop de pyglet
# - r0.5 :
#		- classe pour le canvas.
#		- timer géré
#		- animation

##--- IMPORTS ------------------------------------------------------------------------------
import pyglet
from pyglet import window
from pyglet import clock
from pyglet import font
from pyglet.gl    import *
from pyglet.window import key
from obgeom import Point, SimpleLine, SimpleRec

##--- CONSTANTS ----------------------------------------------------------------------------

drawing_list=[]
frames_tick=1.0/25.0 # pas de division d'int dont le resultat serait 0 !!!
sound_tick=5
sound1 = pyglet.resource.media('tt.wav', streaming=False)
 
##--- CANVAS --------------------------------------------------------------------------------

class Canvas(pyglet.window.Window):
	
	def __init__(self):
		
		window.Window.__init__(self,fullscreen=True)
		
		glShadeModel(GL_SMOOTH)	# Enables smooth shading
		glClearColor(0.0, 0.0, 0.0, 0.0) #Black background
		
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
	
	def draw(self):
		# Here we do all the drawing
		glClear(GL_COLOR_BUFFER_BIT |GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()	
		glColor3f(0.5, 0.5, 1.0)	# set the color to sky-blue  
		#pyglet.gl.glColor4f(0.23,0.23,0.23,1.0) # gray
	
		for lmnt in drawing_list:
			lmnt.pygDraw()      # --- PYGLET OUTPUT
			print(lmnt)         # --- TEXT OUTPUT
			#obgeom.pdfy()      # --- PDF OUTPUT
			#obgeom.dxfy()      # --- DXF OUTPUT
			#obgeom.rhinofy()   # --- RHINO OUTPUT
			#obgeom.imagify()   # --- IMAGE OUTPUT
	
		# ... update and render ...
		print 'FPS is %f' % clock.get_fps()
		# The ``dt`` value returned gives the number of seconds (as a float) since the last "tick".
		# The `get_fps` function averages the framerate over a sliding window of approximately 1 second.
		# (You can calculate the instantaneous framerate bytaking the reciprocal of ``dt``).

		return pyglet.event.EVENT_HANDLED

	def timed_sound(self,deltaT):
		sound1.play()
	
	def update(self, dt):
		geom_update(dt)
		self.draw()

##--- SPECIFIC DRAWING HERE ------------------------------------------------------------------------
def init_layer():
    a = Point(10,10)
    b = Point(100,180)
    c = Point(310, 490)
    testline = SimpleLine(a,b)
    testrec = SimpleRec(100,180,200,300)	# x, y, width, height
    #  | Y
    #  |     X
    #  0 -----
    
    drawing_list.append(c)
    drawing_list.append(testline)
    drawing_list.append(testrec)

def geom_update(dt):
	for lmnt in drawing_list:
		lmnt.move(1,0)
		


##--- MAIN ----------------------------------------------------------------------------------------
if __name__ == "__main__":
	
	calc = Canvas()
	init_layer()

	pyglet.clock.schedule_interval(calc.update, frames_tick)
	pyglet.clock.schedule_interval(calc.timed_sound, sound_tick)
	
	pyglet.app.run()



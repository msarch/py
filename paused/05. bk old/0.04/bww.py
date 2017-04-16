#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : draws rectangles...

# r0.4

#--------------------------------------
#              comments
#--------------------------------------
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
#       - pour l'instant, affiche une liste de géométrie.
# - r0.4 :
#		- utilisation de l'event loop de pyglet

##--- IMPORTS ----------------------------------------------------------------------------------------

import pyglet
from pyglet.gl    import *
from pyglet.image import Texture
from pyglet.window import *

from obgeom import Point, SimpleLine, SimpleRec



##--- CONSTANTS ----------------------------------------------------------------------------------------

drawing_list=[]
window = pyglet.window.Window(width=640, height=480)
pyglet.clock.set_fps_limit(25)

##---PYGLET WINDOW INIT --------------------------------------------------------------------------------

def init():
  	"""
	Pyglet oftentimes calls this setup()	
	"""
  	glShadeModel(GL_SMOOTH)	# Enables smooth shading
	glClearColor(0.0, 0.0, 0.0, 0.0) #Black background
	glClearDepth(1.0)		# Depth buffer setup
	glEnable(GL_DEPTH_TEST)		# Enables depth testing
	glDepthFunc(GL_LEQUAL)		# The type of depth test to do
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)	# Really nice perspective calculations


##---PYGLET WINDOW REDRAW ------------------------------------------------------------------------------
  
@window.event
def on_draw():
  	# Here we do all the drawing
	glClear(GL_COLOR_BUFFER_BIT |GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()	
	#glTranslatef(-1.5, 0.0, -6.0) # Move left 1.5 units and into the screen 6.0
	glColor3f(0.5, 0.5, 1.0)	# set the color to sky-blue  
    #pyglet.gl.glColor4f(0.23,0.23,0.23,1.0) # gray

	for obgeom in drawing_list:
		obgeom.pygDraw()    # --- PYGLET OUTPUT
		print(obgeom)       # --- TEXT OUTPUT
		#obgeom.pdfy()      # --- PDF OUTPUT
		#obgeom.dxfy()      # --- DXF OUTPUT
		#obgeom.rhinofy()   # --- RHINO OUTPUT
		#obgeom.imagify()   # --- IMAGE OUTPUT
		
	return pyglet.event.EVENT_HANDLED


##--- PYGLET WINDOW KEYS HANDLING  -----------------------------------------------------------------
  
@window.event
def on_key_press(symbol, modifiers):
  if symbol == key.RETURN:
	exit()

##--- PYGLET WINDOW UPDATE --------------------------------------------------------------------------
  
def update(dt):
  pass
# Without this the window draw never gets called

##--- CREATE DRAWING LIST --------------------------------------------------------------------------
  
def init_layer():
    a = Point(10,10)
    b = Point(200,400)
    c = Point(300, 8)
    testline = SimpleLine(a,b)
    testrec = SimpleRec(100,180,200,300)	# x, y, width, height
    #  | Y
    #  |     X
    #  0 -----
    
    drawing_list.append(c)
    drawing_list.append(testline)
    drawing_list.append(testrec)


if __name__ == "__main__":
  init()
  init_layer()
  pyglet.app.run()
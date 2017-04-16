from pyglet.gl import *
import pyglet
from pyglet.window import *
"""
When you draw on a window in pyglet, you are drawing to an OpenGL context.
Every window has its own context, which is created when the window is created.
You can access the window's context via its context attribute.
"""

window = pyglet.window.Window(width=640, height=480, resizable=True)

@window.event
def on_key_press(symbol, modifiers):
  if symbol == key.RETURN:
		exit()

def update(dt):
  	pass
# Without this the window draw never gets called
pyglet.clock.schedule(update)

@window.event
def on_resize(width, height):
	if height==0:
		height = 1
	glViewport(0, 0, width, height)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	# Calculate the aspect ratio of the window
	gluPerspective(45.0, 1.0*width/height, 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	return pyglet.event.EVENT_HANDLED

	
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


@window.event
def on_draw():
  	# Here we do all the drawing
	glClear(GL_COLOR_BUFFER_BIT |GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()	

	glTranslatef(-1.5, 0.0, -6.0) # Move left 1.5 units and into the screen 6.0
	
	glBegin(GL_TRIANGLES)
	glColor3f(1.0, 0.0, 0.0)	# set the color to red
	glVertex3f(0.0, 1.0, 0.0)
	glColor3f(0.0, 1.0, 0.0)	# set the color to green
	glVertex3f(-1.0, -1.0, 0.0)
	glColor3f(0.0, 0.0, 1.0)	# set the color to blue
	glVertex3f(1.0, -1.0, 0.0)
	glEnd()

	glTranslatef(3.0, 0.0, 0.0) # Move right 3 units

	glColor3f(0.5, 0.5, 1.0)	# set the color to sky-blue

	# Draw a quad, in a clockwise direction
	glBegin(GL_QUADS)
	glVertex3f(-1.0, 1.0, 0.0)	# Top left
	glVertex3f(1.0, 1.0, 0.0)	# Top right
	glVertex3f(1.0, -1.0, 0.0)	# bottom right
	glVertex3f(-1.0, -1.0, 0.0)	# bottom left
	glEnd()


	return pyglet.event.EVENT_HANDLED
  	
	

init()	

pyglet.app.run()

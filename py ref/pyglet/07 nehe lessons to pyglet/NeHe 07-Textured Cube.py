from pyglet.gl import *
import pyglet
from pyglet.window import *
from pyglet import image
import os
"""
When you draw on a window in pyglet, you are drawing to an OpenGL context. Every window has its own context, which is created when the window is created. You can access the window's context via its context attribute.
"""

window = pyglet.window.Window(width=640, height=480, resizable=True)

xrot=yrot=0.0	# rotate the cube
xspeed=0	# x rot speed
yspeed=0	# y rot speed
z=-5.0		# depth into the screen

filter = 0	# filter to apply (one of 0, 1, 2)

light=True	# lighting on/off
lp=True		# L pressed?
fp=True		# F pressed?

# Ambient light values
LightAmbient = (GLfloat*4)(0.5, 0.5, 0.5, 1.0)
# Bright diffuse light
LightDiffuse = (GLfloat*4)(1.0, 1.0, 1.0, 1.0)
# Light position
LightPosition = (GLfloat*4)(0.0, 0.0, 2.0, 1.0)

def load_gl_textures():
	# load bitmaps and convert to textures
	global textures
	texture_file = os.path.join('data', 'crate.bmp')

	texture_surf = image.load(texture_file)

	# Create a nearest filtered texture
	t1 = texture_surf.get_image_data().create_texture(image.Texture)
	glBindTexture(GL_TEXTURE_2D, t1.id)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	
	# Create a linear filtered texture
	t2 = texture_surf.get_image_data().create_texture(image.Texture)
	glBindTexture(GL_TEXTURE_2D, t2.id)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

	# Create a MipMapped texture
	t3 = texture_surf.get_mipmapped_texture()
	glBindTexture(GL_TEXTURE_2D, t3.id)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

	textures=[t1, t2, t3]



@window.event
def on_key_press(symbol, modifiers):
  global filter, light, z, xspeed, yspeed

  if symbol == key.RETURN or symbol == key.ESCAPE:
		exit()
  elif symbol == key.F:
		filter += 1
		if filter > 2:
		 	filter = 0
  elif symbol == key.L:
		light = not light
		if not light:
		  	glDisable(GL_LIGHTING)
		else:
		  	glEnable(GL_LIGHTING)
  elif symbol == key.PAGEUP:
		z-=0.2
  elif symbol == key.PAGEDOWN:
  		z+=0.2
  elif symbol == key.UP:
  	xspeed += 0.5
  elif symbol == key.DOWN:
  	xspeed -= 0.5
  elif symbol == key.RIGHT:
  	yspeed += 0.5
  elif symbol == key.LEFT:
  	yspeed -= 0.5

def update(dt):
  	global xrot, yrot
	xrot+=xspeed
	yrot+=yspeed


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
	glEnable(GL_TEXTURE_2D)
	load_gl_textures()

  	glShadeModel(GL_SMOOTH)	# Enables smooth shading
	glClearColor(0.0, 0.0, 0.0, 0.0) #Black background
	
	glClearDepth(1.0)		# Depth buffer setup
	glEnable(GL_DEPTH_TEST)		# Enables depth testing
	glDepthFunc(GL_LEQUAL)		# The type of depth test to do

	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)	# Really nice perspective calculations

	glLightfv(GL_LIGHT1, GL_AMBIENT, LightAmbient)	# setup ambient light
	glLightfv(GL_LIGHT1, GL_DIFFUSE, LightDiffuse)	# setup diffuse light
	glLightfv(GL_LIGHT1, GL_POSITION, LightPosition)
	glEnable(GL_LIGHT1)	# enable light one



@window.event
def on_draw():
  	# Here we do all the drawing
	glClear(GL_COLOR_BUFFER_BIT |GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()	

	glTranslatef(0.0, 0.0, z) # translate in/out of screen by z
	
	glRotatef(xrot, 1.0, 0.0, 0.0)
	glRotatef(yrot, 0.0, 1.0, 0.0)

	red = (1.0, 0.0, 0.0)
	green = (0.0, 1.0, 0.0)
	blue = (0.0, 0.0, 1.0)
	orange = (1.0, 0.5, 0.0)
	yellow = (1.0, 1.0, 0.0)
	violet=(1.0, 0.0, 1.0)


	glBindTexture(GL_TEXTURE_2D, textures[filter].id)

	glBegin(GL_QUADS)
	# Front Face
	glNormal3f(0.0, 0.0, 1.0)	# normal pointing towards the viewer
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, 1.0)  # bottom left
	glTexCoord2f(1.0, 0.0); glVertex3f(1.0, -1.0, 1.0) #bottom right
	glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0, 1.0) #top right
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, 1.0) #top left
	
	# Back Face
	glNormal3f(0.0, 0.0, -1.0)	# normal pointing away from viewer
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)	# Bottom Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)	# Bottom Left Of The Texture and Quad
	
	# Top Face
	glNormal3f(0.0, 1.0, 0.0)	# normal pointing up
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)	# Bottom Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)	# Bottom Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
	
	# Bottom Face
	glNormal3f(0.0, -1.0, 0.0)	# normal pointing down
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)	# Top Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)	# Top Left Of The Texture and Quad
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
	
	# Right face
	glNormal3f(1.0, 0.0, 0.0)	# normal pointing right
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)	# Bottom Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
	
	# Left Face
	glNormal3f(-1.0, 0.0, 0.0)	# normal pointing left
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)	# Bottom Left Of The Texture and Quad
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
	glEnd()

	#return pyglet.event.EVENT_HANDLED
  	
init()	

pyglet.app.run()

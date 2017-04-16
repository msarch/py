#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 04.2013
# what : main pyglet engine

# land
# rev 13

##  IMPORTS -----------------------------------------------------------------

import pyglet
from pyglet.gl import *
from pyglet.window import key

##  CONSTANTS AND VARIABLES ---------------------------------------------------

	entities = None
	"""Set of all entities that exist in the world"""

##  CANVAS --------------------------------------------------------------------
class World(mode.Mode):
	"""A coordinated collection of components, systems and entities
    """

	components = None
	""":class:`ComponentParts` object containing all world components.
	:class:`grease.component.Component` objects define and contain all entity data
	"""

	systems = None
	""":class:`Parts` object containing all world systems.
	:class:`grease.System` objects define world and entity behavior
	"""

	renderers = None
	""":class:`Parts` object containing all world renderers.
	:class:`grease.Renderer` objects define world presentation
	"""



class Land(pyglet.window.Window):

    def __init__(self):
        pyglet.window.Window.__init__(self,fullscreen=True)
        self.set_mouse_visible(False)
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        self.xmax = screen.width
        self.ymax = screen.height
        self.xc = (self.xmax*0.5)+1
        self.yc = (self.ymax*0.5)+1
        glClearColor(0.0, 0.0, 0.0, 0.0) # set background color to black
        #glClearColor(1.0, 1.0, 1.0, 1.0) # set background color to white
        glLoadIdentity() # reset transformation matrix
        glTranslatef(self.xc,self.yc,0.0)   # Move Origin to screen center
        self.time=0

        # schedule the update function, 60 times per second
        pyglet.clock.schedule_interval(self.update, 1.0/60.0)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:exit()
        if symbol == key.SPACE:pause=not(pause)

    def on_mouse_press(self,x,y,button,modifiers):
        print x,y
        exit()

    def on_draw(self):
	    """Clear the current OpenGL context, reset the model/view matrix and
	    invoke the `draw()` methods of the renderers in order
	    """
	    glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glClear(GL_STENCIL_BUFFER_BIT)
	    glLoadIdentity()
        for z in self.zulus:
            z.shape.draw()

    def append(self,z):
        self.zulus.append(z)

    def remove(self, z):
        self.zulus.remove(z)

    def live(self, pause=None):
        """ Opens the application windows and starts drawing the canvas.
        """
        #TODO : implementer une pause avec 'space'; voir grease?
        pyglet.app.run()

    def update(self,dt):
        """ This method does not actually draw anything.
		It executes a time step for the world's entities.

		Note that the specified time delta will be pinned to 10x the
		configured step rate. For example if the step rate is 60,
		then dt will be pinned at a maximum of 0.1666. This avoids
		pathological behavior when the time between steps goes
		much longer than expected.

		:param dt: The time delta since the last time step
		:type dt: float
		"""
		dt = min(dt, 10.0 / self.step_rate)
        self.time += dt

# --> FIXME
        for z in self.zulus:
            for rule in z.rules:
                if callable(rule):
                    rule(self,dt)
                else :
                    print 'err'
# --> FIXME
		for component in self.components:
			if hasattr(component, "step"):
				component.step(dt)

        print 'fr', self.frame
        print self.time

    def render(self):
        """ Returns a screenshot of the current frame as a texture.
            This texture can be passed to the image() command.
        """
        return pyglet.image.get_buffer_manager().get_color_buffer().get_texture()

    def save(self, path):
        """ Exports the current frame as a PNG-file.
        """
        pyglet.image.get_buffer_manager().get_color_buffer().save(path)


##--- CANVAS ENTITIES BASE CLASS -------------------------------------------

class Zulu(object):
	""" Zulus objects themselves are merely identifiers of canvas entities.
	They do not contain any data themselves other than an entity id.

	Entities must be instantiated, constructor arguments can be
	specified arbitarily by the subclass.
	"""

    def __init__(self, **kwargs):
        self.rules=None
        self.shape=None
        self.position=None
        self.update=None
        pass


#--- RULES ---------------------------------------------------

class Rules(object):

    def update(self,dt, **kwargs):
        """ do one step.
        """
        pass

class Move(Rule):
    def __init__(zulu,posx,posy,vx=0,vy=0,dt):
        pass

class Listen(Rule):
    def __init__ (self, **kwargs):
        """ parse available data.
        """
        pass

class Publish(Rule):
    def __init__(self, **kwargs):
        """ broadcast data.
        """
        pass


class Position(Component):
	"""Predefined component that stores position and orientation info for
	entities.

	Fields:

	- **position** (Vec2d) -- Position vector
	- **angle** (float) -- Angle, in degrees
	"""

	def __init__(self):
		Component.__init__(self, position=Vec2d, angle=float)


class Transform(Component):
	"""Predefined component that stores offset, shear,
	rotation and scale info for entity shapes.

	Fields:

	- **offset** (Vec2d)
	- **shear** (Vec2d)
	- **rotation** (float)
	- **scale** (float, default 1.0)
	"""

	def __init__(self):
		Component.__init__(self, offset=Vec2d, shear=Vec2d, rotation=float, scale=float)
		self.fields['scale'].default = lambda: 1.0


class Movement(Component):
	"""Predefined component that stores velocity,
	acceleration and rotation info for entities.

	Fields:

	- **velocity** (Vec2d) -- Rate of change of entity position
	- **accel** (Vec2d) -- Rate of change of entity velocity
	- **rotation** (Vec2d) -- Rate of change of entity angle, in degrees/time
	"""

	def __init__(self):
		Component.__init__(self, velocity=Vec2d, accel=Vec2d, rotation=float)


class Shape(Component):
	"""Predefined component that stores shape vertices for entities

	- **closed** (bool) -- If the shapes is closed implying an edge between
	  last and first vertices.
	- **verts** (Vec2dArray) -- Array of vertex points
	"""

	def __init__(self):
		Component.__init__(self, closed=int, verts=Vec2dArray)
		self.fields['closed'].default = lambda: 1


class Renderable(Component):
	"""Predefined component that identifies entities to be
	rendered and provides their depth and color.

	- **depth** (float) -- Drawing depth, can be used to determine z-order
		  while rendering.
	- **color** (color.RGBA) -- Color used for entity. The effect of this
		  field depends on the renderer.
	"""

	def __init__(self):
		Component.__init__(self, depth=float, color=color.RGBA)
		self.fields['color'].default = lambda: color.RGBA(1



class Shape(object):

    def draw(self, **kwargs):
        """ draw to screen,
        should be defined by each subclass
        """
        pass

    def matrix_apply(self,M):
        """ applies matrix M transformation
        to all transformable vertex, incl the centroid.
        """
        for index, vtx in enumerate(self.vtx):
            self.vtx[index] = [self.M[0]*vtx[0]+self.M[1]*vtx[1]+self.M[2],\
                             self.M[3]*vtx[0]+self.M[4]*vtx[1]+self.M[5]]



#!/usr/bin/env python
#

#############################################################################
# STRUCTURE
#############################################################################

class World(mode.Mode):

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

	entities = None
	"""Set of all entities that exist in the world"""



	def __init__(self, step_rate=60, master_clock=pyglet.clock,
				 clock_factory=pyglet.clock.Clock):
		super(World, self).__init__(step_rate, master_clock, clock_factory)
		self.components = ComponentParts(self)
		self.systems = Parts(self)
		self.renderers = Parts(self)
		self.new_entity_id = itertools.count().next
		self.new_entity_id() # skip id 0
		self.entities = WorldEntitySet(self)
		self._full_extent = EntityExtent(self, self.entities)
		self._extents = {}
		self.configure()


wishes=[]

##  CLASSES (LEVEL 1) -------------------------------------------------------------------

class Component(dict):

    def __init__(self):
        wishes.append(self)

    def pygdraw(self,outputdevice="pyglet_canvas"):
        pass

    def timestep(self,dt):
        """Update the component for the next timestep"""
        delitem = super(Component, self).__delitem__
        for entity in self._deleted:
            delitem(entity)
        self.new_entities = self._added
        self.deleted_entities = self._deleted
        self._added = []
        self._deleted = []

    def destroy(self,alive=True):
        pass

    deleted_entities = ()
    """List of entities deleted from the component since the last time step"""

    new_entities = ()
    """List of entities added to the component since the last time step"""

##  CLASSES (LEVEL ) -------------------------------------------------------------------

class Position(Component):
	"""Predefined component that stores position and orientation info for
	entities.

	Fields:

	- **position** (Vec2d) -- Position vector
	- **angle** (float) -- Angle, in degrees
	"""

	def __init__(self):
		Component.__init__(self, position=Vec2d, angle=float)


class Rect(Shape):
    """ rectangle is defined by center x,y and size w,h
    """
    def __init__(self, width=300, height=100):


    def pygdraw(self, **kwargs):
        """ Draws the rectangle with the bottom left corner at x, y.
        The current stroke, strokewidth and fill color are applied.
        """

        pyglet.gl.glColor3f(self.color[0],self.color[1],self.color[2])
        glBegin(GL_QUADS)
        glVertex3f(self.v[1][0], self.v[1][1], 0.0)  # bottom left
        glVertex3f(self.v[2][0], self.v[2][1], 0.0)  # bottom right
        glVertex3f(self.v[3][0], self.v[3][1], 0.0)  # top right
        glVertex3f(self.v[4][0], self.v[4][1], 0.0)  # top left
        glEnd()

class Position(Component):
	"""Predefined component that stores position and orientation info for
	entities.

	Fields:

	- **position** (Vec2d) -- Position vector
	- **angle** (float) -- Angle, in degrees
	"""

	def __init__(self):
		Component.__init__(self, position=Vec2d, angle=float)


class Shape(Component):
	"""Predefined component that stores shape vertices for entities

	- **closed** (bool) -- If the shapes is closed implying an edge between
	  last and first vertices.
	- **verts** (Vec2dArray) -- Array of vertex points
	"""

	def __init__(self):
		Component.__init__(self, closed=int, verts=Vec2dArray)
		self.fields['closed'].default = lambda: 1

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
		self.fields['color'].default = lambda: color.RGBA(1,1,1,1)


class Collision(Component):
	"""Predefined component that stores collision masks to determine
	which entities can collide.

	Fields:

	- **aabb** (Rect) -- The axis-aligned bounding box for the entity.
		This is used for broad-phase collision detection.

	- **radius** (float) -- The collision radius of the entity, used for narrow-phase
		collision detection. The exact meaning of this value depends on the collision
		system in use.

	- **from_mask** (int) -- A bitmask that determines what entities this object
		can collide with.

	- **into_mask** (int) -- A bitmask that determines what entities can collide
		with this object.

	When considering an entity A for collision with entity B, A's ``from_mask`` is
	bit ANDed with B's ``into_mask``. If the result is nonzero (meaning 1 or more
	bits is set the same for each) then the collision test is made. Otherwise,
	the pair cannot collide.

	The default value for both of these masks is ``0xffffffff``, which means that
	all entities will collide with each other by default.
	"""
	def __init__(self):
		Component.__init__(self, aabb=Rect, radius=float, from_mask=int, into_mask=int)
		self.fields['into_mask'].default = lambda: 0xffffffff
		self.fields['from_mask'].default = lambda: 0xffffffff


class SlideX(Dynamics):

    def step(self.dt): # this methods holds dynamics for the component
        """Execute a time step for the object.
        Note that the specified time delta will be pinned to 10x the
        configured step rate. For example if the step rate is 60,
        then dt will be pinned at a maximum of 0.1666. This avoids
        pathological behavior when the time between steps goes
        much longer than expected.
        """
            global hfac
            self.transform()
            if (self.v[1][0]<cl or self.v[2][0]>cr):    # if bounce,
               # a.M[2] *=-1                            # reverse dir
                self.color = choice(kapla_colors)       # change clr
                self.M[2] *= hfac                       # vary H speed
                hfac=1.0/hfac




class SlideY(Dynamics):

    def __init__(self):
        Rec.__init__(self, width=300, height=100, xc=0, yc=0, \
             color=(0,0,0), M=id_matrix()):

    def step(self.dt):
        global vfac
    for a in actors2 :
        a.transform()
        if (a.v[4][1]>ct or a.v[1][1]<cb):  # if bounce,
            #a.M[5] *=-1                         # reverse dir
            a.color = choice(kapla_colors)      # change clr
            a.M[5] *= vfac                         # change speed
            vfac=1.0/vfac
            tintors2_update()
            tintors3_update()


#############################################################################
# SCENE
#############################################################################


# methode step
class Gun(grease.System):

    def step(self, dt):
        for entity in self.world[...].gun.firing == True:
            if self.world.time >= entity.gun.last_fire_time + entity.gun.cool_down:
                Shot(self.world, entity, entity.position.angle)
                if entity.gun.sound is not None:
                    entity.gun.sound.play()
                entity.gun.last_fire_time = self.world.time

# methode step / fade et disparition
class Sweeper(grease.System):
    """Clears out space debris"""

    def step(self, dt):
        fade = dt / self.SWEEP_TIME
        for entity in tuple(self.world[Debris].entities):
            color = entity.renderable.color
            if color.a > 0.2:
                color.a = max(color.a - fade, 0)
            else:
                entity.delete()

# renderer, no init method?

class Hud(grease.Renderer):
    """Heads-up display renderer"""

    def draw(self):
        game = self.world.systems.game
        if self.last_lives != game.lives:
            for i, entity in self.lives:
                if game.lives > i:
                    entity.renderable.color = PlayerShip.COLOR
                else:
                    entity.renderable.color = (0,0,0,0)
            self.last_lives = game.lives
        if self.last_score != game.score:
            self.score_label = pyglet.text.Label(
                str(game.score),
                color=(180, 180, 255, 255),
                font_name='Vector Battle', font_size=14, bold=True,
                x=window.width // 2 - 25, y=window.height // 2 - 25,
                anchor_x='right', anchor_y='center'

# entité de base, init method

class Asteroid(grease.Entity):
    """Big floating space rock"""


    def __init__(self, world, radius=45):
        self.position.position = (
            random.choice([-1, 1]) * random.randint(50, window.width / 2),
            random.choice([-1, 1]) * random.randint(50, window.height / 2))
        self.movement.velocity = (random.gauss(0, 700 / radius), random.gauss(0, 700 / radius))
        self.movement.rotation = random.gauss(0, 15)
        verts = [(random.gauss(x * radius, radius / 7), random.gauss(y * radius, radius / 7))
            for x, y in self.UNIT_CIRCLE]
        self.shape.verts = verts
        self.renderable.color = "#aaa"


def main():

		for component in self.components:
			if hasattr(component, "step"):
				component.step(dt)
		for system in self.systems:
			if hasattr(system, "step"):
				system.step(dt)

	def on_draw(self, gl=pyglet.gl):
		"""Clear the current OpenGL context, reset the model/view matrix and
		invoke the `draw()` methods of the renderers in order
		"""
		gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
		gl.glLoadIdentity()
		for renderer in self.renderers:
			renderer.draw()



if __name__ == '__main__':
    main()

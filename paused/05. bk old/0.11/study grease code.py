#############################################################################
# GREASE EXTCERPTS
#############################################################################


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


	def tick(self, dt):
		"""Tick the mode's clock, but only if the world is currently running

		:param dt: The time delta since the last tick
		:type dt: float
		"""
		if self.running:
			super(World, self).tick(dt)

	def step(self, dt):

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





##  CLASSES (LEVEL 1) -------------------------------------------------------------------

class Component(dict):
	"""General component with a configurable schema

	The field schema is defined via keyword args where the
	arg name is the field name and the value is the type object.

	The following types are supported for fields:

	- :class:`int`
	- :class:`float`
	- :class:`bool`
	- :class:`str`
	- :class:`object`
	- |Vec2d|
	- |Vec2dArray|
	- |RGBA|
	- |Rect|
	"""

	deleted_entities = ()
	"""List of entities deleted from the component since the last time step"""

	new_entities = ()
	"""List of entities added to the component since the last time step"""

	def __init__(self, **fields):
		self.fields = {}
		for fname, ftype in fields.items():
			assert ftype in field.types, fname + " has an illegal field type"
			self.fields[fname] = field.Field(self, fname, ftype)
		self.entities = ComponentEntitySet(self)
		self._added = []
		self._deleted = []


	def step(self, dt):
		"""Update the component for the next timestep"""
		delitem = super(Component, self).__delitem__
		for entity in self._deleted:
			delitem(entity)
		self.new_entities = self._added
		self.deleted_entities = self._deleted
		self._added = []
		self._deleted = []

	def set(self, entity, data=None, **data_kw):
		"""Set the component data for an entity, adding it to the
		component if it is not already a member.

		If data is specified, its data for the new entity's fields are
		copied from its attributes, making it easy to copy another
		entity's data. Keyword arguments are also matched to fields.
		If both a data attribute and keyword argument are supplied for
		a single field, the keyword arg is used.
		"""
		if data is not None:
			for fname, field in self.fields.items():
				if fname not in data_kw and hasattr(data, fname):
					data_kw[fname] = getattr(data, fname)
		data = self[entity] = Data(self.fields, entity, **data_kw)
		return data

	def __setitem__(self, entity, data):
		assert entity.world is self.world, "Entity not in component's world"
		if entity not in self.entities:
			self._added.append(entity)
			self.entities.add(entity)
		super(Component, self).__setitem__(entity, data)

	def remove(self, entity):
		if entity in self.entities:
			self._deleted.append(entity)
			self.entities.remove(entity)
			return True
		return False

	__delitem__ = remove

	def __repr__(self):
		return '<%s %x of %r>' % (
			self.__class__.__name__, id(self), getattr(self, 'world', None))







##  CLASSES (LEVEL 2) -------------------------------------------------------------------


class Position(Component):
	"""Predefined component that stores position and orientation info for
	entities.

	Fields:

	- **position** (Vec2d) -- Position vector
	- **angle** (float) -- Angle, in degrees
	"""

	def __init__(self):
		Component.__init__(self, position=Vec2d, angle=float)



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


#############################################################################
# GREASE.RENDERER EXTCERPTS
#############################################################################




class Vector(object):
	"""Renders shapes in a classic vector graphics style

	:param scale: Scaling factor applied to shape vertices when rendered.

	:param line_width: The line width provided to ``glLineWidth`` before rendering.
		If not specified or None, ``glLineWidth`` is not called, and the line
		width used is determined by the OpenGL state at the time of rendering.

	:param anti_alias: If ``True``, OpenGL blending and line smoothing is enabled.
		This allows for fractional line widths as well. If ``False``, the blending
		and line smoothing modes are unchanged.

	:param corner_fill: If true (the default), the shape corners will be filled
		with round points when the ``line_width`` exceeds 2.0. This improves
		the visual quality of the rendering at larger line widths at some
		cost to performance. Has no effect if ``line_width`` is not specified.

	:param position_component: Name of :class:`grease.component.Position`
		component to use. Shapes rendered are offset by the entity positions.

	:param renderable_component: Name of :class:`grease.component.Renderable`
		component to use. This component specifies the entities to be
		rendered and their base color.

	:param shape_component: Name of :class:`grease.component.Shape`
		component to use. Source of the shape vertices for each entity.

	The entities rendered are taken from the intersection of he position,
	renderable and shape components each time :meth:`draw` is called.
	"""

	CORNER_FILL_SCALE = 0.6
	CORNER_FILL_THRESHOLD = 2.0

	def __init__(self, scale=1.0, line_width=None, anti_alias=True, corner_fill=True,
		position_component='position',
		renderable_component='renderable',
		shape_component='shape'):
		self.scale = float(scale)
		self.corner_fill = corner_fill
		self.line_width = line_width
		self.anti_alias = anti_alias
		self._max_line_width = None
		self.position_component = position_component
		self.renderable_component = renderable_component
		self.shape_component = shape_component

	def set_world(self, world):
		self.world = world

	def _generate_verts(self):
		"""Generate vertex and index arrays for rendering"""
		vert_count = sum(len(shape.verts) + 1
			for shape, ignored, ignored in self.world.components.join(
				self.shape_component, self.position_component, self.renderable_component))
		v_array = (CVertColor * vert_count)()
		if vert_count > 65536:
			i_array = (ctypes.c_uint * 2 * vert_count)()
			i_size = pyglet.gl.GL_UNSIGNED_INT
		else:
			i_array = (ctypes.c_ushort * (2 * vert_count))()
			i_size = pyglet.gl.GL_UNSIGNED_SHORT
		v_index = 0
		i_index = 0
		scale = self.scale
		rot_vec = Vec2d(0, 0)
		for shape, position, renderable in self.world.components.join(
			self.shape_component, self.position_component, self.renderable_component):
			shape_start = v_index
			angle = radians(-position.angle)
			rot_vec.x = cos(angle)
			rot_vec.y = sin(angle)
			r = int(renderable.color.r * 255)
			g = int(renderable.color.g * 255)
			b = int(renderable.color.b * 255)
			a = int(renderable.color.a * 255)
			for vert in shape.verts:
				vert = vert.cpvrotate(rot_vec) * scale + position.position
				v_array[v_index].vert.x = vert.x
				v_array[v_index].vert.y = vert.y
				v_array[v_index].color.r = r
				v_array[v_index].color.g = g
				v_array[v_index].color.b = b
				v_array[v_index].color.a = a
				if v_index > shape_start:
					i_array[i_index] = v_index - 1
					i_index += 1
					i_array[i_index] = v_index
					i_index += 1
				v_index += 1
			if shape.closed and v_index - shape_start > 2:
				i_array[i_index] = v_index - 1
				i_index += 1
				i_array[i_index] = shape_start
				i_index += 1
		return v_array, i_size, i_array, i_index

	def draw(self, gl=pyglet.gl):
		vertices, index_size, indices, index_count = self._generate_verts()
		if index_count:
			if self.anti_alias:
				gl.glEnable(gl.GL_LINE_SMOOTH)
				gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
				gl.glEnable(gl.GL_BLEND)
				gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
			gl.glPushClientAttrib(gl.GL_CLIENT_VERTEX_ARRAY_BIT)
			gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
			gl.glEnableClientState(gl.GL_COLOR_ARRAY)
			gl.glVertexPointer(
				2, gl.GL_FLOAT, ctypes.sizeof(CVertColor), ctypes.pointer(vertices))
			gl.glColorPointer(
				4, gl.GL_UNSIGNED_BYTE, ctypes.sizeof(CVertColor),
				ctypes.pointer(vertices[0].color))
			if self.line_width is not None:
				gl.glLineWidth(self.line_width)
				if self._max_line_width is None:
					range_out = (ctypes.c_float * 2)()
					gl.glGetFloatv(gl.GL_ALIASED_LINE_WIDTH_RANGE, range_out)
					self._max_line_width = float(range_out[1]) * self.CORNER_FILL_SCALE
				if self.corner_fill and self.line_width > self.CORNER_FILL_THRESHOLD:
					gl.glEnable(gl.GL_POINT_SMOOTH)
					gl.glPointSize(
						min(self.line_width * self.CORNER_FILL_SCALE, self._max_line_width))
					gl.glDrawArrays(gl.GL_POINTS, 0, index_count)
			gl.glDrawElements(gl.GL_LINES, index_count, index_size, ctypes.pointer(indices))
			gl.glPopClientAttrib()




class Camera(object):
	"""Sets the point of view for further renderers by altering the
	model/view matrix when it is drawn. It does not actually perform
	any drawing itself.

	:param position: The position vector for the camera. Sets the center of the view.
	:type position: Vec2d
	:param angle: Camera rotation in degrees about the z-axis.
	:type angle: float
	:param zoom: Scaling vector for the coordinate axis.
	:type zoom: Vec2d
	:param relative: Flag to indicate if the camera settings are relative
		to the previous view state. If ``False`` the view state is reset before
		setting the camera view by loading the identity model/view matrix.

	At runtime the camera may be manipulated via attributes with the
	same names and functions as the parameters above.
	"""

	def __init__(self, position=None, angle=None, zoom=None, relative=False):
		self.position = position
		self.angle = angle
		self.zoom = zoom
		self.relative = relative

	def draw(self, gl=pyglet.gl):
		if not self.relative:
			gl.glLoadIdentity()
		if self.position is not None:
			px, py = self.position
			gl.glTranslatef(px, py, 0)
		if self.angle is not None:
			gl.glRotatef(self.angle, 0, 0, 1)
		if self.zoom is not None:
			sx, sy = self.zoom
			gl.glScalef(sx, sy ,0)


#############################################################################
# BLASTEROID EXTCERPTS
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

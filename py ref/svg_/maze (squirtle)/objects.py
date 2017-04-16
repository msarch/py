def script():
	Objects.stage.win.set_caption('Mazes')
	views.append(View(x=0,y=0,width=Objects.stage.win.width,height=Objects.stage.win.height, window=Objects.stage.win))

	views.append(View(x=0,y=0,width=256,height=256, window=Objects.stage.win, scale=0.2))
	#views.append(View(x=Objects.stage.win.width-256,y=Objects.stage.win.height-256,width=256,height=256, window=Objects.stage.win, scale=0.2))
	views.append(View(x=0,y=Objects.stage.win.height-256,width=256,height=256, window=Objects.stage.win, scale=0.2))
	views.append(View(x=Objects.stage.win.width-256,y=0,width=256,height=256, window=Objects.stage.win, scale=0.2))


class GameMenu(object):

	def __init__(self, stage):
		self.stage = stage
		self.selection = 0

		pyglet.clock.schedule_interval(self.update, 0.125)

		self.label_new_game = pyglet.text.Label("New Game",
			font_name='Tahoma Arial',
			font_size=16,
			x=0,
			y=32,
			anchor_x='center',
			anchor_y='center',
			color=(128, 128, 128, 255))
		self.label_continue = pyglet.text.Label("Continue",
			font_name='Tahoma Arial',
			font_size=16,
			x=0,
			y=64,
			anchor_x='center',
			anchor_y='center',
			color=(128, 128, 128, 255))
		self.label_quit = pyglet.text.Label("Quit",
			font_name='Tahoma Arial',
			font_size=16,
			x=0,
			y=96,
			anchor_x='center',
			anchor_y='center',
			color=(128, 128, 128, 255))

	def back(self):
		pyglet.clock.unschedule(self.update)
		pyglet.clock.schedule_interval(self.stage.update, 0.016)

		self.stage.win.remove_handlers(self)
		self.stage.win.push_handlers(self.stage)

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.UP:
			self.selection += 1
		elif symbol == pyglet.window.key.DOWN:
			self.selection -= 1
		if symbol == pyglet.window.key.ENTER:
			if self.selection is 1:
				self.back()
				self.stage.setStage()
			elif self.selection is 2:
			    self.back()
			elif self.selection is 3:
				pyglet.app.exit()
				#sys.exit()
		if symbol == pyglet.window.key.ESCAPE:
		    self.back()
		    return pyglet.event.EVENT_HANDLED

	def update(self, dt):
		if self.selection == 0:
			self.selection = 3
		elif self.selection == 4:
			self.selection = 1

		self.label_new_game.color=(128, 128, 128, 255)
		self.label_continue.color=(128, 128, 128, 255)
		self.label_quit.color=(128, 128, 128, 255)

		if self.selection == 1:
			self.label_new_game.color=(0, 0, 128, 255)
		elif self.selection == 2:
			self.label_continue.color=(0, 0, 128, 255)
		elif self.selection == 3:
			self.label_quit.color=(0, 0, 128, 255)

		self.stage.win.invalid = True

	def on_draw(self):
		glLoadIdentity()
		glTranslatef(self.stage.win.width / 2, self.stage.win.height / 2, 0.0)

		#The quad is needed for the font to look nice otherwise a call to glClear or stage.draw would be needed.
		glColor4ub(64, 64, 64, 255)
		glBegin(GL_QUADS)
		glVertex3f(-128, -128, 0.0)
		glVertex3f(128, -128, 0.0)
		glVertex3f(128, 128, 0.0)
		glVertex3f(-128, 128, 0.0)
		glEnd()

		self.label_new_game.draw()
		self.label_continue.draw()
		self.label_quit.draw()


class HUD(Objects):
	label = pyglet.text.Label('FPS counter eventually?',
		font_name='Arial',
		font_size=16,
		x=512,
		y=256,
		anchor_x='center',
		anchor_y='center',
		color=(128, 0, 128, 255))
	def __init__(self):
		pass

	def __del__(self):
		pass

	def draw():
		label.draw()


class Player(Objects, pyglet.window.key.KeyStateHandler):
	image = squirtle.SVG(gfxBaseDir + 'player.svg', anchor_x = 'center', anchor_y = 'center')
	def create(self):
		self.width = 128
		self.height = 256

		self.keyring=[]

		bodyDef = box2d.b2BodyDef()
		bodyDef.position = (self.x / self.RATIO, self.y / self.RATIO)
		bodyDef.fixedRotation = True
		self.body = self.world.CreateBody(bodyDef)

		self.body.SetUserData(self)

		shapeDef = box2d.b2PolygonDef()
		shapeDef.SetAsBox(64 / self.RATIO, 128 / self.RATIO)
		#shapeDef.density = 1.0
		shapeDef.friction = 0.0
		#shapeDef.restitution = 0.01
		shape=self.body.CreateShape(shapeDef)

		shapeDef2 = box2d.b2CircleDef()
		shapeDef2.SetUserData("feet")
		shapeDef2.radius = 1.5
		shapeDef2.density = 1.0
		shapeDef2.localPosition.Set(0.0, -4.0)
		shapeDef2.isSensor = True
		shape=self.body.CreateShape(shapeDef2)

		self.body.SetMassFromShapes()

		views[0].follow=self
		views[1].follow=self
		views[2].follow=self
		views[3].follow=self

	def update(self):
		if  self.keyboard[pyglet.window.key.UP]:
			if Objects.collision(self, Ladder):
				self.vel = self.body.GetLinearVelocity()
				self.vel = self.body.GetLinearVelocity()
				self.body.SetLinearVelocity(box2d.b2Vec2(self.vel.x,4))

		if  self.keyboard[pyglet.window.key.SPACE]:
			if self.isInACollision("feet"):
				self.vel = self.body.GetLinearVelocity()
				self.body.SetLinearVelocity(box2d.b2Vec2(self.vel.x,8))
			elif self.isInACollision("feet"):
				self.vel = self.body.GetLinearVelocity()
				self.body.SetLinearVelocity(box2d.b2Vec2(self.vel.x,8))

		self.vel = self.body.GetLinearVelocity()

		if self.keyboard[pyglet.window.key.RIGHT]:
			#f = self.body.GetWorldVector((400.0, 0.0))
			#p = self.body.GetWorldPoint((400.0, 0.0))
			#self.body.ApplyForce(f, p)
			#self.body.ApplyImpulse(f, p)
			#self.body.WakeUp()
			self.body.SetLinearVelocity(box2d.b2Vec2(16,self.vel.y))
			#print self.body.GetWorldCenter()
			#self.body.position.x =+ 10
		elif  self.keyboard[pyglet.window.key.LEFT]:
			self.body.SetLinearVelocity(box2d.b2Vec2(-16,self.vel.y))
		else:
			self.body.SetLinearVelocity(box2d.b2Vec2(0,self.vel.y))

		if  self.keyboard[pyglet.window.key.DOWN]:
			self.instanceCreate(Ladder, self.x, self.y, self.world)

		if self.keyboard[pyglet.window.key.ESCAPE]:
			pyglet.clock.unschedule(Objects.stage.update)
			Objects.stage.win.remove_handlers(Objects.stage)
			Objects.stage.win.push_handlers(GameMenu(Objects.stage))

		#if Objects.collision(self, Ladder):
		if self.placeMeeting(Ladder):
			self.other.instanceChange(Player)

		if Objects.collision(self, Key):
			self.keyring.append(self.other.IDtag)
			print "Got key number", self.other.IDtag

		position = self.body.GetPosition();
		self.x = position.x * self.RATIO
		self.y = position.y * self.RATIO

	def draw(self):
		Player.image.draw(self.x, self.y, angle=(self.body.GetAngle() * 180 / 3.141592))


class Ladder(Objects):
	def create(self):
		self.width = 64
		self.height = 256

		bodyDef = box2d.b2BodyDef()
		bodyDef.position = (self.x / self.RATIO, self.y / self.RATIO)
		bodyDef.fixedRotation = True
		self.body = self.world.CreateBody(bodyDef)

		self.body.SetUserData(self)

		shapeDef = box2d.b2PolygonDef()
		shapeDef.SetAsBox(64 / self.RATIO, 128 / self.RATIO)
		shapeDef.isSensor = True
		shape=self.body.CreateShape(shapeDef)


class Key(Objects):
	#image = squirtle.SVG(gfxBaseDir + 'key.svg', anchor_x = 'center', anchor_y = 'center')
	def __init__(self, x, y, world):
		self.x = x
		self.y = y
		self.width = 32
		self.height = 32
		self.IDtag = tag

	def draw(self):
		self.image.draw(self.x, self.y)


class Door(Objects):
	#image = squirtle.SVG(gfxBaseDir + 'door.svg', anchor_x = 'center', anchor_y = 'center')
	def __init__(self, x, y, world):
		self.x = x
		self.y = y
		self.width = 32
		self.height = 32
		self.IDtag = tag

	def draw(self):
		self.image.draw(self.x, self.y)


class LevelExit(Objects):
	def __init__(self):
		pass
		# will need to pass colision detection box

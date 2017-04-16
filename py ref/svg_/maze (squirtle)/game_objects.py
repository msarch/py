import pyglet
import Box2D as box2d
import squirtle

gfxBaseDir = 'gfx/'

# The whole resource loading system may have to be reworked this would this would be a good way to do it:
# def load_images():
#     images = {}
#
#     for filename in os.listdir('images'):
#         key = filename.split('.')[0]
#         value = pyglet.image.load(os.sep.join(['images', filename]))
#
#         images[key] = value
#
#     return images


#3. loop: objectys.draw, objects{"player"}.draw
#explosion = pyglet.media.load('exp.wav', streaming=False)
#explosion.play()

#Use **kwargs for extra arguments like ID/SECTOR TAG or ladder width/height?

class Objects(object):
	"""Bass class for game objects.
	I am atempting make the object system as easy to use as Game Makers,
	This class also acts as an interface between the engine and the game.
	"""

	RATIO = 32
	gContacts = []
	gObjects = []
	world = None
	keys = pyglet.window.key.KeyStateHandler()
	stage = None
	views = None

	def __init__(self, x, y, direction=0, tag=None, custom={}):
		for (name, value) in custom.items():
			self.__dict__[name] = value

		self.x = x
		self.y = y
		try:
			self.width = self.image.width
			self.height = self.image.height
		except:
			self.draw = self.empty
		self.other = None
		self.direction = direction

		self.world = Objects.world#Should not need this, instead have world as global base class var
		#gObjects.apped(self)

		if tag != None:
			self.tag = tag

		self.keyboard = Objects.keys

		self.create()

	def create(self):
		pass

	def destroy(self):
		pass

	def update(self):
		pass

	def draw(self):
		self.image.draw(self.x, self.y, angle=self.direction)

	def empty(self):
		pass

	@staticmethod #Needed to get rid of unbound method error
	def getObjectDefs():
		ObjectDefs={}
		for i in Objects.__subclasses__():
			ObjectDefs[i.__name__.lower()]=i
		return ObjectDefs

	def placeMeeting(self, target):
		#print type(caller), type(target)
		for pair in Objects.gContacts:
			#print type(pair.shape2.GetBody().GetUserData()), type(pair.shape1.GetBody().GetUserData())
			if (pair.shape1.GetBody().GetUserData()) is self and isinstance(pair.shape2.GetBody().GetUserData(), target):#Type check instead of plain == caller, but not type check for target(need to be exact here)
				self.other = pair.shape2.GetBody().GetUserData()
				return True
			elif (pair.shape2.GetBody().GetUserData()) is self and isinstance(pair.shape1.GetBody().GetUserData(), target):
				self.other = pair.shape1.GetBody().GetUserData()
				return True

	def collisionObjects(self, caller, target):
		pass

	def collision(caller, target):
		#print type(caller), type(target)
		for pair in Objects.gContacts:
			#print type(pair.shape2.GetBody().GetUserData()), type(pair.shape1.GetBody().GetUserData())
			if type(pair.shape1.GetBody().GetUserData()) == type(caller) and isinstance(pair.shape2.GetBody().GetUserData(), target):#Type check instead of plain == caller, but not type check for target(need to be exact here)
				caller.other = pair.shape2.GetBody().GetUserData()
				return True
			elif type(pair.shape2.GetBody().GetUserData()) == type(caller) and isinstance(pair.shape1.GetBody().GetUserData(), target):
				caller.other = pair.shape1.GetBody().GetUserData()
				return True
		return False

	def isInACollision(self, target):
		for pair in Objects.gContacts:
			if pair.shape1.GetUserData() is target:
				return True
			if pair.shape2.GetUserData() is target:
				return True

	def findAttributeValue(self, attrib, value):
		for obj in Objects.gObjects:
			if hasattr(obj, attrib):
				if getattr(obj, attrib) == value: # Replacing with "is"
					self.other = obj
					return True
		return False

	def instanceCreate(self, obj, x, y, world):
		newObject = obj(x, y)
		Objects.gObjects.append(newObject)
		return obj

	@staticmethod
	def instanceCreate2(obj, x, y, custom):
		newObject = obj(x, y, custom=custom)
		Objects.gObjects.append(newObject)
		return newObject

	def instanceChange(self, newObject):
		self.instanceCreate(newObject, self.x, self.y, self.world)
		self.instanceDestroy()

	def instanceDestroy(self):
		self.destroy()

		self.body.SetUserData(None)
		self.world.DestroyBody(self.body)
		self.body = None

		Objects.gObjects.remove(self)
		self.other = None

	def setController(self, x=0, y=0, width=0, height=0, scale=1, background=(255,255,255,255)):
		views.append(View(x=0,y=0,width=self.win.width,height=self.win.height, window=Objects.stage.win))

#!/usr/bin/python2.6
"""
MAZES
Benjamin Debski <benjamin.debski@gmail.com>
started 16th?/October/2008
"""

import os, sys, time
sys.stdout = sys.__stdout__
sys.path += ['.']
from xml.dom import minidom
import xml.etree.ElementTree

import pyglet
#pyglet.options['debug_gl'] = False
from pyglet.gl import *
import Box2D as box2d
import squirtle
import libsvg2b2d
from game_objects import *

mapsBaseDir = 'levels/'

class Contact:
	shape1 = None
	shape2 = None
	normal = None
	position = None
	velocity = None
	id = None
	state = 0


class ContactListener(box2d.b2ContactListener):
	def __init__(self):
		Objects.gContacts=[]
		super(ContactListener, self).__init__()

	def createContact(self, state, point):
		#if not self.test: return
		cp = Contact()
		cp.shape1 = point.shape1
		cp.shape2 = point.shape2
		cp.normal = point.normal
		cp.position = point.position
		cp.velocity = point.velocity
		cp.id = point.id
		cp.state = state
		Objects.gContacts.append(cp)

	def Add(self, point):
		pass

	def Persist(self, point):
		self.createContact(2, point)
		pass

	def Remove(self, point):
		pass #Need to fix constant collisions between player and player
		"""try:
			Objects.gContacts.remove(point)
		except:
			print "FUCKED UP"
		"""

	def getContacts():
		return self.test


class FPS(object):

	def __init__(self):
		self.lastUpdate = 0
		self.currentUpdate = 0
		self.fps = 0
		self.frames = 0
		self.label = pyglet.text.Label("Calculating FPS",
			font_name='Tahoma Arial',
			font_size=16,
			x=0,
			y=0,
			anchor_x='right',
			anchor_y='top',
			color=(128, 128, 128, 255))
		if(sys.platform == 'win32' or sys.platform == 'win64'):
			self.timer = time.clock
		else:
			self.timer = time.time

	#def update(self, viewX, viewY):
	def update(self):
		#self.label.x = viewX-10
		#self.label.y = viewY+120
		#views[0].update()
		#self.label.x = views[0].right-50
		#self.label.y = views[0].top-50
		##self.label.x = views[0].follow.x-10
		##self.label.y = views[0].follow.y+120

		self.frames += 1
		self.currentUpdate = self.timer()

		if self.currentUpdate - self.lastUpdate > 1.0:
			self.fps = self.frames
			self.label.text = str(self.fps)
			self.frames = 0
			self.lastUpdate = self.currentUpdate

	def draw(self):
		if views[0].current is True:
			self.label.x = views[0].right-32
			self.label.y = views[0].top-32
			self.label.draw()


class Scene(object):
	def __init__(self):
		self.objectDefs = Objects.getObjectDefs()
		self.mapList = sorted(os.listdir('levels'))
		#self.mapList.sort()
		self.mapIndex = 0
		self.RATIO = 32

		self.displayMapList()
		self.set()

		self.timeStep = 1.0 / 60.0 #Could change for slowmotion powerup
		self.velocityIterations = 10
		self.positionIterations = 8

	def displayMapList(self):
		print "\nMaps found:", len(self.mapList)
		print "Map list:",
		for map in self.mapList:
			print map,
		print "\n"

	def set(self):
		#print "MAP INDEX = ", self.mapIndex, "MAP SELECTION = ", selection

		#self.mapIndex = selection
		if self.mapIndex > (len(self.mapList) - 1):
			self.mapIndex = 0
		elif self.mapIndex < 0:
			self.mapIndex = (len(self.mapList) - 1)

		Objects.gObjects=[]
		self.map = squirtle.SVG(mapsBaseDir + self.mapList[self.mapIndex])

		self.world = libsvg2b2d.SVG2B2D(file = mapsBaseDir + self.mapList[self.mapIndex], ratio = self.RATIO)

		self.contactListener = ContactListener()
		self.world.SetContactListener(self.contactListener)

		Objects.world = self.world

		self.spawnObjects()

	def goto(self, level):
		self.level = level + ".svg"

	def reload(self):
		Objects.gObjects=[]
		self.spawnObjects()

	def spawnObjects(self):
		objectKeys = self.objectDefs.keys()
		for obj in libsvg2b2d.LoadSVG.objectList:
			if obj['label'] in objectKeys:
				newObject = Objects.instanceCreate2(self.objectDefs[obj['label']], obj['x'] + obj['width'] / 2, obj['y'] - obj['height'] / 2, custom=obj['custom'])
			else:
				print "No class matching object:", obj['label']

	def update(self):
		self.world.Step(self.timeStep, self.velocityIterations, self.positionIterations)

	def draw(self):
		self.map.draw(0, 0, 0, 0, scale=1)


class dummy:
	def __init__(self):
		self.x = 0
		self.y = 0

	def update(self):
		pass

	def draw(self, *args, **kwargs):
		pass


views=[]


class View(object):
	def __init__(self, x=0, y=0, width=0, height=0, follow=dummy(), scale=1, background=(255,255,255,255), window=None):
		if window is None:#Should not neet this test automatically pass window in the GO wrapper
			print "No Window, no view"
			return
		if width%2 is not 0 or height%2 is not 0:
			raise UserWarning, 'glViewport width and height must be even'#FIXME, does not seam to work anymore?
			return 1

		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.follow = follow
		self.scale = scale
		self.background = background
		self.window = window
		self.current = False
		self.top = self.follow.y + self.height / 2
		self.bottom = self.follow.y - self.height / 2
		self.left = self.follow.x - self.width / 2
		self.right = self.follow.x + self.width / 2

	def update(self):
		pass
		#self.__dict__['top'] = self.__dict__['follow.y'] - self.__dict__['height'] / 2

	def __getattribute__(self, attr):
		follow = object.__getattribute__(self,  'follow')
		height = object.__getattribute__(self,  'height')
		width = object.__getattribute__(self,  'width')
		if attr == 'top':
			return follow.y + height / 2
		if attr == 'bottom':
			return follow.y - height / 2
		if attr == 'left':
			return follow.x - width / 2
		if attr == 'right':
			return follow.x + width / 2

		return object.__getattribute__(self,  attr)


class Stage(object):
	def __init__(self):
		self.zoom = 1.0

		self.createWindow()

		self.FPSCounter = FPS()
		self.showFPS = False

		Objects.stage=self
		Objects.views=views
		try:
			script()
		except:
			pass

		self.win.push_handlers(Objects.keys)
		self.scene = dummy()

		pyglet.clock.unschedule(self.update)
		pyglet.clock.schedule_interval(self.update, 0.016)
		self.setStage()
		pyglet.app.run()

	def setStage(self):
		self.win.remove_handlers(self)

		Objects.gObjects = []
		self.scene = Scene()

		self.win.push_handlers(self)

	def newConfig(self):
		defaultConfig = {'width':'1024',
			'height':'768',
			'fullscreen':'False',
			'bpp':'32',
			'vsync':'True',
			'multisampling':'0',
			'linewidth':'1',
			'mousevisible':'False'}
		if(sys.platform != 'win32' and sys.platform != 'win64'):
			defaultConfig['depth'] = '24'

		return defaultConfig

	def createWindow(self):
		Stage.cfg = cfg = self.newConfig()
		print "Config path:", GameOptions.filePath
		GameOptions.readFile(cfg)
		for setting in cfg:
			print "\t", setting, '=', cfg[setting]

		template = Config(double_buffer=True,
		buffer_size=int(cfg['bpp']),
		sample_buffers=0,
		samples=int(cfg['multisampling']))

		if int(cfg['multisampling'])>0:
			template.sample_buffers = 1

		self.win = pyglet.window.Window(width=int(cfg['width']),
		height=int(cfg['height']),
		caption='untitled',
		vsync=eval(cfg['vsync']),
		config=template)

		self.win.set_fullscreen(eval(cfg['fullscreen']))
		self.win.set_mouse_visible(eval(cfg['mousevisible']))

		self.win.push_handlers(self)

		glPointSize(1)
		glEnable(GL_BLEND)
		glLineWidth(int(cfg['linewidth']))
		glScissor((self.win.width - 800) / 2, (self.win.height - 600) / 2, 800, 600)#Set window size on any monitor

		@self.win.event
		def on_key_press(symbol, modifiers):
			if symbol is pyglet.window.key.ESCAPE:
				#print len(self.win._event_stack)
				return True

	def bodyCount(self):
		bodyList = self.scene.world.GetBodyList()
		for body in bodyList:
			print "User data", type(body.GetUserData()), "User data =", body.GetUserData()
		print "Body count =", len(bodyList)

	def on_key_press(self, symbol, modifiers):
		if symbol is pyglet.window.key.ESCAPE:
			pass

		if symbol == pyglet.window.key.F12:
			self.win.set_fullscreen(not self.win.fullscreen)
			glScissor((self.win.width - 800) / 2, (self.win.height - 600) / 2, 800, 600)

		if symbol == pyglet.window.key.F8:
			if self.FPSCounter in Objects.gObjects:
				Objects.gObjects.remove(self.FPSCounter)
			else:
				Objects.gObjects.append(self.FPSCounter)

		if symbol == pyglet.window.key.PAGEUP:
			self.scene.mapIndex += 1
			self.scene.set()
		elif symbol == pyglet.window.key.PAGEDOWN:
			self.scene.mapIndex -= 1
			self.scene.set()

		if symbol == pyglet.window.key.F9:
			self.bodyCount()
			print("OBJECTS OBJECT LIST", len(Objects.gObjects))
			print("M11 OBJECT LIST", len(Objects.gObjects))

		if symbol == pyglet.window.key.F11:
			pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')
			print("SCREENSHOT TAKEN")

		if symbol == pyglet.window.key.GRAVE:
			GameConsole(self)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		self.zoom += (scroll_y * 0.02)

	def drawQuad(self, i=None):
		glColor4ub(255, 0, 128, 128)
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

		for i in Objects.gObjects:
			glBegin(GL_QUADS)
			glVertex3f(i.x - i.width / 2, i.y - i.width, 0.0)
			glVertex3f(i.x + i.width / 2, i.y - i.width, 0.0)
			glVertex3f(i.x + i.width / 2, i.y + i.height / 2, 0.0)
			glVertex3f(i.x - i.width / 2 , i.y + i.height / 2, 0.0)
			glEnd()

		glBegin(GL_QUADS)
		glVertex3f(i.x - i.width / 2, i.y - i.width, 0.0)
		glVertex3f(i.x + i.width / 2, i.y - i.width, 0.0)
		glVertex3f(i.x + i.width / 2, i.y + i.height / 2, 0.0)
		glVertex3f(i.x - i.width / 2 , i.y + i.height / 2, 0.0)
		glEnd()

		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

	def drawVector(self, object):
		glColor4ub(255, 0, 0, 255)
		for i in object:
			glBegin(GL_LINES)
			glVertex3f(i['x'], i['y'], 0.0)
			glVertex3f(i['x2'], i['y2'], 0.0)
			glEnd()

	def update(self, dt):
		self.scene.update()

		for obj in Objects.gObjects:
			obj.update()
		Objects.gContacts=[]#Need to fix constant collisions between player and player

		self.win.invalid = True

	def on_draw(self):
		glClearColor(0, 0 ,0 , 255)
		glClear(GL_COLOR_BUFFER_BIT)

		if self.win.fullscreen is True:#Optimize, only needs to be calculated on resize or the addition of a new view
			viewWidthMax = 0
			viewHeightMax = 0
			for view in views:
				if view.width > viewWidthMax:
					viewWidthMax = view.width
				if view.height > viewHeightMax:
					viewHeightMax = view.height

			viewOffsetX = self.win.width / 2 - viewWidthMax / 2
			viewOffsetY = self.win.height / 2 - viewHeightMax / 2
		else:
			viewOffsetX = 0
			viewOffsetY = 0

		for view in views:
			glViewport(viewOffsetX + view.x, viewOffsetY + view.y, view.width, view.height)#Add in room for AA(should this be after reseting the projection matrix?)
			glMatrixMode(GL_PROJECTION)#Reset coordinate system before modifying it
			glLoadIdentity()
			gluOrtho2D(viewOffsetX + view.x, viewOffsetX + view.x + view.width, viewOffsetY + view.y, viewOffsetY + view.y + view.height)

			glMatrixMode(GL_MODELVIEW)
			glLoadIdentity()

			glScissor(viewOffsetX + view.x, viewOffsetY + view.y, view.width, view.height)#Limit clear
			glEnable(GL_SCISSOR_TEST)
			glClearColor(view.background[0],view.background[1],view.background[2],view.background[3])
			glClear(GL_COLOR_BUFFER_BIT)
			glDisable(GL_SCISSOR_TEST)

			#HUD drawing could go here?

			#glTranslatef(-self.controller.x * self.zoom + view.x + (view.width/2), -self.controller.y * self.zoom + view.y + (view.height/2), 0.0)
			#glTranslatef(-self.controller.x * (self.zoom*view.scale) + view.x + (view.width/2), -self.controller.y * (self.zoom*view.scale) + view.y + (view.height/2), 0.0)
			glTranslatef(-view.follow.x * (self.zoom*view.scale) + view.x + (view.width/2) + viewOffsetX, -view.follow.y * (self.zoom*view.scale) + view.y + (view.height/2) + viewOffsetY, 0.0)
			glScalef(self.zoom*view.scale , self.zoom*view.scale , self.zoom)

			view.current = True
			#glPushMatrix()
			self.scene.draw()
			for obj in Objects.gObjects:
				obj.draw()
			#glPopMatrix()
			view.current = False

		#Need to set this to window cord not view in case a view does not exist, special case fullscreen
		glViewport(0, 0, self.win.width, self.win.height)#Add in room for AA(should this be after reseting the projection matrix?)
		glMatrixMode(GL_PROJECTION)#Reset coordinate system before modifying it
		glLoadIdentity()
		gluOrtho2D(0, self.win.width, 0, self.win.height)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		#Overlay HUD drawing could go here?

		self.win.invalid = False


class GameConsole(object):

	def __init__(self, stage):
		self.stage = stage

		pyglet.clock.unschedule(self.stage.update)
		self.stage.win.remove_handlers(self.stage)
		self.stage.win.push_handlers(self)

		pyglet.clock.schedule_interval(self.update, 0.125)#8 CPS

		self.labelConsole = pyglet.text.Label('\r',
			font_name='Tahoma Arial',
			font_size=16,
			x=4,
			y=self.stage.win.height / 1.5,
			anchor_x='left',
			anchor_y='bottom',
			color=(64, 255, 64, 255),
			#multiline=True,
			width = 320
			)

		self.log = pyglet.text.document.UnformattedDocument("\n\n\n\n\n\n\n\n\n\n")

		self.log.styles["font"]='Tahoma Arial'
		self.log.styles["font_size"]=16
		self.log.styles["color"]=(64, 128, 64, 255)
		self.log.styles["wrap"]=True

		self.logLayout = pyglet.text.layout.IncrementalTextLayout(self.log, self.stage.win.width, self.stage.win.height / 3, multiline=True)
		self.logLayout.x = 4
		self.logLayout.y = self.stage.win.height
		self.logLayout.anchor_x='left'
		self.logLayout.anchor_y='top'
		print self.logLayout.content_width
		#self.logLayout.content_valign='bottom'

		self.stdout = sys.stdout
		sys.stdout = self

	def write(self, s):
		self.log.text = self.log.text + s
		while self.log.text.count("\n") > 40:
			self.removeLine()

	def removeLine(self):
		self.log.text = self.log.text[(self.log.text.find("\n")+1):]

	def update(self, dt):
		self.stage.win.invalid = True
		self.logLayout.view_y = -1024

	def on_text(self, char):
		if char != "`":
			self.labelConsole.text += char

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.BACKSPACE:
			self.labelConsole.text = self.labelConsole.text[:-1]

		if symbol == pyglet.window.key.ENTER:
			print self.labelConsole.text
			if self.labelConsole.text[0] == "\r":
				self.labelConsole.text = self.labelConsole.text[1:]
			try:
				exec(self.labelConsole.text)
			except Exception as inst:
				print type(inst)
				print inst.args
				print inst

			self.labelConsole.text = str()
			#self.logLayout.view_y = -1024
			#self.logLayout.ensure_line_visible(self.log.text.count("\n"))

		if symbol == pyglet.window.key.GRAVE:
			pyglet.clock.unschedule(self.update)
			pyglet.clock.schedule_interval(self.stage.update, 0.016)

			self.stage.win.remove_handlers(self)
			self.stage.win.push_handlers(self.stage)

			sys.stdout = self.stdout

		if symbol is pyglet.window.key.PAGEUP:
			self.logLayout.view_y += 8

		if symbol is pyglet.window.key.PAGEDOWN:
			self.logLayout.view_y -= 8

	def on_draw(self):
		self.stage.on_draw()
		glLoadIdentity()

		glColor4ub(128, 128, 128, 128)
		glBegin(GL_QUADS)
		glVertex3f(self.stage.win.width, self.stage.win.height / 1.5, 0.0)
		glVertex3f(self.stage.win.width, self.stage.win.height, 0.0)
		glVertex3f(0, self.stage.win.height, 0.0)
		glVertex3f(0, self.stage.win.height / 1.5, 0.0)
		glEnd()

		self.labelConsole.draw()
		self.logLayout.draw()


class GameOptions(object):
	#filePath = os.path.join("Z:\\", 'config.txt')
	filePath = os.path.join(os.path.expanduser('~'), 'config.txt')
	print filePath

	@staticmethod
	def writeFile(config):
		print("Saving config")
		configFile = open(GameOptions.filePath, 'w')
		for item in config.keys():
			configFile.write(item+'='+config[item]+'\n')
		configFile.close()

	@staticmethod
	def readFile(settings={}):
		print("Loading config:")
		if not os.path.isfile(GameOptions.filePath):
			return False

		configFile = open(GameOptions.filePath, 'r')
		line = configFile.readline()
		while line:
			val = line.split('=')
			key = val[0]
			settings[key] = val[1][:-1]
			line = configFile.readline()

		configFile.close()

		return settings


# * * * ENTRY POINT HERE * * *
print "Python version:", sys.version
print "Pyglet version:", pyglet.version
print "Pybox2D version:", box2d.__version__
print "OpenGL version:", pyglet.gl.gl_info.get_version()
print "OpenGL vendor:", pyglet.gl.gl_info.get_vendor()
print "OpenGL renderer:", pyglet.gl.gl_info.get_renderer()
print "--------------------------------------------------------------------------------"

if os.path.isfile("objects.py"):
	execfile("objects.py", globals(), locals())
	#exec(compile(open("objects.py").read(), "objects.py", 'exec'), globals(), locals())

if __name__=="__main__":
	Stage()
	GameOptions.writeFile(Stage.cfg)

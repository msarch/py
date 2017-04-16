
'''

	Project:	CS100
	Title:		Renderer

	Author:		John Mooney
	Date:		2/26/2013

	Description:
		Prepares and Renders OpenGL frame
'''


# Imports
from pyglet.gl import (glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)

from Object import Object
from SceneGraph import SceneGraph
from Camera import Camera
from tools import getDictValue
from TransformationGraph import Transform


#------------------------------------------------------#

class Renderer(Object):

	activeRenderer = None
	
	def __initP__(self, **kwArgs):
		super().__initP__(**kwArgs)
		
		self._sceneGraph 	= SceneGraph()
		self._camera 		= Camera(getDictValue(kwArgs, None, ['ws', 'winSize', 'windowSize'], True), t=Transform())

		self._camera.focus()
		
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def render(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		self._camera.focus()
		self._camera.view()
		self._sceneGraph.draw()
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	@classmethod
	def getRenderer(cls):
		return cls.activeRenderer
	
	def setSceneGraph(self, sg):
		self._sceneGraph = sg
	def getSceneGraph(self):
		return self._sceneGraph
		
	def setCamera(self, c):
		self._camera = c
	def getCamera(self):
		return self._camera
	
		
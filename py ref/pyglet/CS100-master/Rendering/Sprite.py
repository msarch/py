
'''

	Project:	CS100
	Title:		Sprite

	Author:		John Mooney
	Date:		3/29/2013

	Description:
		An on screen image instance
'''

# Imports
import pyglet.image
from pyglet.gl import *

from Animation import Animation
from SceneObject import SceneObject
from Transformable import Transformable
from AnimationState import AnimationState
from DiscretePrimitives import DiscreteRect


class Sprite(Transformable):

	def __init__(self, imageSrc, **kwArgs):
		super().__init__(**kwArgs)

		#	Set Image/Animation
		if isinstance(imageSrc, Animation):
			self._animation = AnimationState(imageSrc)
			self._texture = self._animation.getImage().get_texture()
		else:
			self._animation = None
			self._texture = imageSrc.get_texture()
			
		#	Create the Scene Object representation
		self._sceneObject = SceneObject(dataSrc = DiscreteRect(self._texture.width, self._texture.height),	\
			t=self.getTransform(), ed=[('t3f', self._texture.tex_coords)], batch=kwArgs.get('batch', None), group=kwArgs.get('group', None))
		self._sceneObject.isDrawn = False
		
	''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def update(self, dt):
		if self._animation and self._animation.update(dt):
			self._texture = self._animation.getImage().get_texture()
	
	def draw(self):
		glBindTexture(self._texture.target, self._texture.id)
		glEnable(self._texture.target)
		
		self._sceneObject.draw()
		
		glDisable(self._texture.target)

	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def getImage(self):
		return self._texture
		
	def setAnimation(self, animState):
		self._animation.setState(animState)
	def getAnimation(self):
		return self._animation

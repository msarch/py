
'''

	Project:	CS100
	Title:		CollisionWorld

	Author:		John Mooney
	Date:		4/21/2013

	Description:
		Handles collision detection on all collision primitives
'''


# Imports
from Object import Object
from Renderer import Renderer
from SceneObject import SceneObject
from Transformable import Transformable
from CollisionPrimitives import CollisionRect

import Color

#-------------------------------------------------#

class Entity(Transformable):
	
	def __init__(self, sprite, **kwArgs):
		super().__init__(**kwArgs)

		self._sprite = sprite
		self._sprite.getAnimation().setState("Looping")
		self._sprite.setTransform(self.getTransform().createChild())
		
		self._collider = CollisionRect(self._sprite.getImage().width, self._sprite.getImage().height, t=self.getTransform().createChild())
		self._collider.addListener(self)
		
		self._boundsDisplay = None
		#self._boundsDisplay = SceneObject(dataSrc = self._collider, t=self._collider.getTransform(), color=Color.Green)

	''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def update(self, dt):
		self._sprite.update(dt)
		self._collider.update(dt)
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def notifyCollisions(self, colliderObj, otherColliders):
		if self._boundsDisplay:
			if otherColliders:
				self._boundsDisplay.setColor(Color.Red)
			else:
				self._boundsDisplay.setColor(Color.Green)


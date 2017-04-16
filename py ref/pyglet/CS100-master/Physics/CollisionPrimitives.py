
'''

	Project:	CS100
	Title:		CollisionPrimitives

	Author:		John Mooney
	Date:		4/21/2013

	Description:
		A basic primitive for determining collision detection
'''


# Imports
from Transformable import Transformable
from DiscretePrimitives import *

#-------------------------------------------------------#

class CollisionPrimitive(Transformable):
	
	def __initP__(self, **kwArgs):
		super().__initP__(**kwArgs)
		
		self._listeners = []
		self._worldPoints = []
		
		
	''''''''''''''''''''''''''''''''''''''''''''''''''
		
	def draw(self):
		pass
	
	
	''''''''''''''''''''''''''''''''''''''''''''''''''
	
	#	Need to calculate values, applying transformations in order to local object
	def _onTransformation(self, transformations):
		newPoints = []
		hasTranslated 	= bool(transformations[0])
		hasRotated 		= bool(transformations[1])
		hasScaled 		= bool(transformations[2])
		
		#	Create Temporaries
		angleSin = 0.0;		angleCos = 0.0
		if hasRotated:	
			angleSin = math.sin(self._worldRot)
			angleCos = math.cos(self._worldRot)
			
			
		#	Apply Transformation
		for point in self._localPoints:
			newPoint = point.copy()
			
			if hasScaled:
				newPoint *= self._worldScale
			if hasRotated:
				newPoint.x = newPoint.x*angleCos - newPoint.y*angleSin
				newPoint.y = newPoint.x*angleSin + newPoint.y*angleCos
			if hasTranslated:
				newPoint += self._worldPos
				
			newPoints.append(newPoint)
			
		self._worldPoints = newPoints
		super()._onTransformation(transformations)
		
		
	''''''''''''''''''''''''''''''''''''''''''''''''''

	def addListener(self, obj):
		self._listeners.append(obj)
	def getWorldPoints(self):
		return self._worldPoints
	def getListeners(self):
		return self._listeners


#---------------------------------------------------------#

class CollisionRect(DiscreteRect, CollisionPrimitive):
	pass

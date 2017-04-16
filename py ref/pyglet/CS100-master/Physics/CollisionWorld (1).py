
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


#-------------------------------------------------#

class CollisionWorld(Object):
	
	def __init__(self, **kwArgs):
		super().__init__(**kwArgs)
		self._collisionPrimitives = []
		
		
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def update(self, dt):
		self._testCollisions()
		
		
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def addPrimitive(self, p):
		self._collisionPrimitives.append(p)
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''
	def _testCollisions(self):
		#	Create lists of AABB Points
		allAABBXVals = []
		allAABBYVals = []
		for cp in self._collisionPrimitives:
			coords = cp.getWorldPoints()
			allAABBXVals.append((coords[0].x, cp));	allAABBXVals.append((coords[1].x, cp))
			allAABBYVals.append((coords[0].y, cp));	allAABBYVals.append((coords[2].y, cp))
		
		#	Get Collision in both Axis
		xCollisions = self._getCollisionsIn(allAABBXVals)
		yCollisions = self._getCollisionsIn(allAABBYVals)

		
		#	Calculate Colliders
		for primitive in self._collisionPrimitives:
			colliderSet = xCollisions.get(primitive, set()).intersection(yCollisions.get(primitive, set()))
			
			for listener in primitive.getListeners():
				listener.notifyCollisions(primitive, colliderSet)

			
	def _getCollisionsIn(self, axisPoints):
		sortedPoints = sorted(axisPoints, key=lambda point:point[0])
		
		#	Find Overlapping Primitive Points
		primColliders = {}
		activePrimitives = []
		for p in sortedPoints:
			primitive = p[1]
			
			#	Handle Entry/Exit for a primitive
			if primitive in activePrimitives:
				activePrimitives.remove(primitive)
			else:
				primColliders[primitive] = set()
				activePrimitives.append(primitive)
			
			#	Set Collision Sets
			for otherPrim in activePrimitives:
				if otherPrim is primitive:
					continue
				primColliders[otherPrim].add(primitive)
				primColliders[primitive].add(otherPrim)
		
		return primColliders

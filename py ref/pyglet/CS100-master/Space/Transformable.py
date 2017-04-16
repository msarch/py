
'''

	Project:	CS100
	Title:		Transformable

	Author:		John Mooney
	Date:		10/22/2012

	Description:
		A Transformable entity within the Game - has a position, rotation, scale in the world
'''

# Imports
from Object import Object

from Vector import vec
from tools import getDictValue

class Transformable(Object):
	
	def __initP__(self, **kwArgs):
		super().__initP__(**kwArgs)
		
		self._transform 	= None
		self._worldPos 		= vec()
		self._worldRot 		= 0.0
		self._worldScale 	= vec(1, 1)
		self._lastTransformation = [False, [0,0,0]]
		
		'''		Temporary Fix		'''
		self.isDrawn = True
		

	def __initC__(self, **kwArgs):
		self._localPos		= getDictValue(kwArgs, vec(), ['lp', 'localPos'])
		self._localRot		= getDictValue(kwArgs, 0.0, ['lr', 'localRot'])
		self._localScale	= getDictValue(kwArgs, vec(1, 1), ['ls', 'localScale'])

		t = getDictValue(kwArgs, None, ['t', 'transform'])
		if(t):
			self.setTransform(t)
			self._onTransformation(self._lastTransformation[1])
		
		super().__initC__(**kwArgs)

	''''''''''''''''''''''''''''''''''''''''''
	
	def update(self, dt):
		if self._lastTransformation[0]:
			self._onTransformation(self._lastTransformation[1])
			

	#################################
	#	Transform Setters/Getters	#
	#################################
	

	def getPosition(self):
		return self._worldPos
	def getRotation(self):
		return self._worldRot
	def getScale(self):
		return self._worldScale
	
	
	'''	Setters '''
	
	def translate(self, v):
		self._transform.translate(v)
	def translate2f(self, x, y):
		self._transform.translate2f(x,y)
	def setTranslation(self, v):
		self._transform.setTranslation(v)
	def setTranslation2f(self, x, y):
		self._transform.setTranslation2f(x,y)
		
	def rotate(self, r):
		self._transform.rotate(r)
	def setRotation(self, r):
		self._transform.setRotation(r)
		
	def scale(self, s):
		self._transform.scale(s)
	def scale2f(self, x, y):
		self._transform.scale2f(x, y)
	def setScale(self, s):
		self._transform.setScale(s)
	def setScale2f(self, x, y):
		self._transform.setScale2f(x, y)

		
	#############################
	#		Getters/Setters		#
	#############################

	def getTransform(self):
		return self._transform
	def setTransform(self, node):
		self._transform = node
		node._addTransformable(self)
	def removeTransform(self):
		t = self._transform
		
		self._transform._removeTransformable(self)
		self._transform = None
		
		self._worldPos 		= vec()
		self._worldRot		= 0.0
		self._worldScale	= vec(1,1)
		
		return t
		
		
	#################################
	#		Data Maintenance		#
	#################################
	
	def _onTransformation(self, transformations):
		self._lastTransformation[0] = False;	self._lastTransformation[1] = [0,0,0]
		

	def _onTranslation(self, dif):
		self._worldPos  	= self._localPos + self._transform.getTranslation()
		self._lastTransformation[0] = True;	self._lastTransformation[1][0] = dif
	def _onRotation(self, dif):
		self._worldRot  	= self._localRot + self._transform.getRotation()
		self._lastTransformation[0] = True;	self._lastTransformation[1][1] = dif
	def _onScale(self, dif):
		self._worldScale 	= self._localScale * self._transform.getScale()
		self._lastTransformation[0] = True;	self._lastTransformation[1][2] = dif
		

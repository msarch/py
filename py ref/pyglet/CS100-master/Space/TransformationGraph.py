	
'''

	Project:	CS100
	Title:		TransformationGraph
	
	Author:		John Mooney
	Date:		10/22/2012

	Description:
		The Main-Game Transform Graph; Handles all transformations within CS100
		
'''

# Imports
from Object import Object

from Vector import vec
from Vector import ZeroVector
from tools import getDictValue

#--------------------------------------------------#

class TransformationGraph(Object):

	def __initP__(self, **kwArgs):
		super().__initP__(**kwArgs)
		self._rootNode = Transform()

		
	''''''''''''''''''''''''''''''''''''''''''
	
	#################################
	#		Accessor Methods		#
	#################################
		
	def getRoot(self):
		return self._rootNode

	def newTransform(self, **kwArgs):
		return self._rootNode.createChild(**kwArgs)
		
'''
	
	Class:		_Transform
	
	Description:
		A scene graph node; Contains Entity and Transform Data
'''

class Transform(Object):

	def __initP__(self, **kwArgs):
		super().__initP__(**kwArgs)
		
		'''	Node and Update Values '''
		self._parent  	= None
		self._children 	= []
		
		'''	Transform Data '''
		self._translate 	= getDictValue(kwArgs, vec(), ['t', 'translate'])
		self._rotateRads 	= getDictValue(kwArgs, 0.0, ['r', 'rotate'])
		self._scale			= getDictValue(kwArgs, vec(1,1), ['s', 'scale'])
		self._gTrans		= self._translate.copy()
		self._gRotRads      = self._rotateRads
		self._gScale		= self._scale.copy()
	
		'''	Transformable Data	'''
		self._transformables  = []

	
	''''''''''''''''''''''''''''''''''''''''''
	
	#############################
	#		Transforms			#
	#############################

	def translate(self, v):
		self._translate += v
		self._translateDependents()
	def translate2f(self, x, y):
		self._translate += vec(x, y)
		self._translateDependents()
	def setTranslation(self, v):
		self._translate = v
		self._translateDependents()
	def setTranslation2f(self, x, y):
		self._translate = vec(x,y)
		self._translateDependents()
		
	def rotate(self, rads):
		self._rotateRads+=rads
		self._rotateDependents()
	def setRotation(self, rads):
		self._rotateRads = rads
		self._rotateDependents()

	def scale(self, v):
		self._scale *= v
		self._scaleDependents()
	def scale2f(self, x, y):
		self._scale *= vec(x,y)
		self._scaleDependents()
	def setScale(self, v):
		self._scale = v
		self._scaleDependents()
	def setScale2f(self, x, y):
		self._scale = vec(x, y)
		self._scaleDependents()
	

	''''''''''''''''''''''''''''''''''''''''''
		
	#########################
	#		Accessors		#
	#########################
	
	def getTranslation(self):
		return self._gTrans.copy()
	def getLocalTranslation(self):
		return self._translate.copy()
		
	def getRotation(self):
		return self._gRotRads
	def getLocalRotation(self):
		return self._rotateRads
		
	def getScale(self):
		return self._gScale.copy()
	def getLocalScale(self):
		return self._scale.copy()
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	#####################################
	#		Common Node Operations		#
	#####################################
	
	def createChild(self, **kwArgs):
		node = Transform(**kwArgs)
		node.setParent(self)
		return node
		
		
	''''''''''''''''''''''''''''''''''''''''''''''''

	#########################################
	#		Transformable Operations		#
	#########################################
	
	def _addTransformable(self, d):
		self._transformables.append(d)
		
		d._onTranslation(self._gTrans)
		d._onRotation(self._gRotRads)
		d._onScale(self._gScale)

	def _removeTransformable(self, d):
		self._transformables.remove(d)
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	#################################
	#		Data Maintenance		#
	#################################
	
	def _translateDependents(self):
		pTrans = vec()
		if(self._parent):
			pTrans = self._parent.getTranslation()
			
		newTranslate = self._translate + pTrans
		oldTranslate = self._gTrans.copy()
		if(newTranslate != oldTranslate):	
			self._gTrans = newTranslate
			
			for transformable in self._transformables:
				transformable._onTranslation(newTranslate-oldTranslate)
			for child in self._children:
				child._translateDependents()
	def _rotateDependents(self):
		pRots = 0.0
		if(self._parent):
			pRots = self._parent.getRotation()
			
		newRot = self._rotateRads + pRots
		oldRot = self._gRotRads
		if(newRot != oldRot):	
			self._gRotRads = newRot
			
			for transformable in self._transformables:
				transformable._onRotation(newRot-oldRot)
			for child in self._children:
				child._rotateDependents()
	def _scaleDependents(self):
		pScale = vec(1.0, 1.0)
		if(self._parent):
			pScale = self._parent.getScale()
			
		newScale = self._scale * pScale
		oldScale = self._gScale
		
		if(newScale != oldScale):
			self._gScale = newScale
			
			for transformable in self._transformables:
				transformable._onScale(newScale/oldScale)
			for child in self._children:
				child._scaleDependents()
				

	def _updateDependents(self):
		self._translateDependents()
		self._rotateDependents()
		self._scaleDependents()
	
	
	''''''''''''''''''''''''''''''''''''''''''''''''
		
	#################################
	#		Noding Operations		#
	#################################
	
	def setParent(self, p):
		self.removeParent()
		self._parent = p
		
		p._children.append(self)
		self._updateDependents()
		
	def removeParent(self):
		if(self._parent):
			self._parent._children.remove(self)
			self._updateDependents()
		self._parent = None

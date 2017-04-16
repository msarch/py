
'''

	Project:	CS100
	Title:		Tree

	Author:		John Mooney
	Date:		4/22/2013

	Description:
		A Tree graph for representing relationships
'''


# Imports


#--------------------------------------------------#

class Tree(Object):
	
	def __init__(self, **kwArgs):
		super().__init__()
		
		self._rootNode = None
		self._injectedComponents = []
	
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def addComponent(self, componentCreator):
		pass
	
	def getRoot(self):
		return self._rootNode
	def newNode(self):
		return self._rootNode.createChild()
		

#--------------------------------------------------#

class Node(Object):

	def __init__(self, **kwArgs):
		super().__init__(**kwArgs)
		
		self._parent = None
		self._children = []
		self._components = []
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def createChild(self):
		n = Node()
		n.setParent(self)
		return n
		
	
	def setParent(self, n):
		if self._parent:
			self._removeParent()
		
		self._parent = n
		self._parent._children.append(self)
		self._updateComponents()
		
	def removeParent(self):
		self._parent._children.remove(self)
		self._parent = None
		self._updateComponents()

		
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def _addComponent(self, componentCreator, kwArgs):
		c = creator(**kwArgs)
		
		c._node = self
		self._components.append(c)
		self._updateComponents()
		
		
	def _updateComponents(self):
		for c in self._components:
			c.update()

'''

	Project:	CS100
	Title:		GeometricPrimitives

	Author:		John Mooney
	Date:		2/26/2013

	Description:
		Represents geometric primitives
'''


# Imports
from Object import Object
from Vector import vec
from tools import getDictValue


#------------------------------------------------------#

class GeometricEllipse(Object):

	def __init__(self, a, b, **kwArgs):
		self._a = vec(a, 0)
		self._b = vec(0, b)
		
		super().__init__(**kwArgs)
		

#------------------------------------------------------#

class GeometricRect(Object):
	
	def __init__(self, w, h, **kwArgs):
		self._width 	= w
		self._height 	= h
		self._diagonal 	= vec(w/2, h/2)
		
		super().__init__(**kwArgs)
		

#------------------------------------------------------#

class GeometricCircle(Object):

	def __init__(self, radius, **kwArgs):
		self._radius = radius
		super().__init__(**kwArgs)
		

#------------------------------------------------------#

class GeometricTriangle(Object):

	def __init__(self, points, **kwArgs):
		self._pVecs	= points
		super().__init__(**kwArgs)
		

#------------------------------------------------------#

class GeometricLine(Object):

	def __init__(self, eVec, **kwArgs):
		self._endVec = eVec
		super().__init__(**kwArgs)
		
		
#------------------------------------------------------#
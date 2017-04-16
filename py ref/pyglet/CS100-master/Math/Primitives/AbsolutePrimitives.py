
'''

	Project:	CS100
	Title:		AbsolutePrimitives

	Author:		John Mooney
	Date:		2/26/2013

	Description:
		Represents geometric shapes as a set of absolute, discrete points
'''

# Imports
from Object import Object


#-----------------------------------------------#

class AbsolutePrimitive(Object):

	def __initC__(self, **kwArgs):
		self.__data = self._points[:]
		super.__initC__(**kwArgs)
	
	
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def _onTranslation(self, dif):
		super()._onTranslation(dif)
		for p in self._points:
			p+=dif
			
	def _onRotation(self, dif):
		super()._onRotation(dif)
		
		c=math.cos(dif);	s=math.sin(dif)
		for v in self.__data:
			v.x = v.x*c - v.y*s
			v.y = v.x*s + v.y*c		

	def _onScale(self, dif):
		super()._onScale(dif)
		for v in self.__data:
			v*=dif
			

#-----------------------------------------------#

class AbsoluteRect(AbsolutePrimitive, DiscreteRect):
	def __initC__(self, **kwArgs):
		self.__data[:] = self.__data+[self._diagonal]
		super().__initC__(**kwArgs)
		
	def _onScale(self, dif):
		super()._onScale(dif)
		self._width *= dif.x
		self._height *= dif.y
		
		
#-----------------------------------------------#

class AbsoluteEllipse(AbsolutePrimitive, DiscreteEllipse):
	def __initC__(self, **kwArgs):
		self.__data[:] = self.__data+[self._a, self._b]
		super().__initC__(**kwArgs)
		
#-----------------------------------------------#

class AbsoluteLine(AbsolutePrimitive, DiscreteLine):
	def __initC__(self, **kwArgs):
		self.__data[:] = self.__data+[self._endVec]
		super().__initC__(**kwArgs)
		
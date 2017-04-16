
'''

	Project:	CS100
	Title:		Vector
	
	Author:		John Mooney
	Date:		06/22/2012

	Description:
		A 2D Vector within Sketch Space. 
'''

# Imports
from Object import Object

from math import sqrt
from math import pow
from math import acos

from tools import *

'''
	Class: 	Vector

		A 2D Vector Class.
	
'''
class vec(Object):
	
	def __init__(self, x=0.0, y=0.0, **kwArgs):
		kwArgs['x'] = x;	kwArgs['y'] = y
		super().__init__(**kwArgs)
		
	def __initP__(self, **kwArgs):
		super().__initP__(**kwArgs)
		
		tx = getDictValue(kwArgs, 0.0, ['x'], True)
		ty = getDictValue(kwArgs, 0.0, ['y'], True)
		
		try:
			self.x = tx.x
			self.y = tx.y
		except AttributeError:
			self.x = float(tx)
			self.y = float(ty)
			

	#########################################
	#	Getter/Setter Methods		#
	#########################################

	def setX(self, x):
		self.x = float(x)
	def setY(self, y):
		self.y = float(y)

	def set(self, v):
		self.x = float(v.x)
		self.y = float(v.y)
	def set2f(self, x, y):
		self.x = float(x)
		self.y = float(y)

	def __setitem__(self, index, val):
		if(index == 0):
			self.x = float(val)
		elif(index == 1):
			self.y = float(val)
		else:
			raise IndexError("Invalid Vector Access: " + str(index))
		
	def __getitem__(self, index):
		if(index == 0):
			return self.x
		elif(index == 1):
			return self.y
		else:
			raise IndexError("Invalid Vector Access: " + str(index))

		
	#########################################
	#	Operational Functions		#
	#########################################
	
	def copy(self):
		return vec(self.x, self.y)
	def length(self):
		return sqrt(self.x*self.x + self.y*self.y)
	def squaredLength(self):
		return self.x*self.x + self.y*self.y
	def rounded(self, digits=0):
		return vec(round(self.x, digits), round(self.y, digits))
	def round(self, digits=0):
		self.x = round(self.x, digits)
		self.y = round(self.y, digits)

	def unit(self):
		m = self.length()
		return vec(self.x/m, self.y/m)
	def unitize(self):
		m = self.length()
		self.x /= m
		self.y /= m

		
	'''	Vector Operations	'''
	def dotP(self, v):
		return self.x*v.x + self.y*v.y
	def getUnitAngleTo(self, vec):
		if (self.y > vec.y):
			return acos(self.dotP(vec))
		else:
			return -acos(self.dotP(vec))
	def getAngleTo(self, vec):
		return self.unit().getUnitAngleTo(vec.unit())
		

	#################################
	#	Vector Operations	#
	#################################

	'''	Vector Operations	'''
	def __add__(self, v):
		return vec(self.x + v.x, self.y + v.y)
	def __sub__(self, v):
		return vec(self.x - v.x, self.y - v.y)
	def __mul__(self, v):
		try:
			return vec(self.x * v.x, self.y * v.y)
		except AttributeError:
			return vec(self.x*v, self.y*v)
	def __truediv__(self, v):
		try:
			return vec(self.x/v.x, self.y/v.y)
		except AttributeError:
			return vec(self.x/v, self.y/v)
			

	''' Identive Operations	'''
	def __iadd__(self, v):
		self.x += v.x
		self.y += v.y
		return self
	def __isub__(self, v):
		self.x -= v.x
		self.y -= v.y
		return self
	def __imul__(self, v):
		try:
			self.x*=v.x
			self.y*=v.y
		except AttributeError:
			self.x*=v
			self.y*=v
		return self
	def __itruediv__(self, v):
		try:
			self.x/=v.x
			self.y/=v.y
		except AttributeError:
			self.x/=v
			self.y/=v
		return self

		
	#################################
	#	Comparison, et all	#
	#################################
	
	def __eq__(self, v):
		if(v == None):
			return False
		else:
			return nearEq(self.x, v[0]) and nearEq(self.y, v[1])
	def __ne__(self, v):
		return not self==v
	def __pos__(self):
		return abs(self)		
	def __neg__(self):
		return vec(-self.x, -self.y)
	def __abs__(self):
		return vec(abs(self.x), abs(self.y))
	def __str__(self):
		return "<" + str(self.x) + ", " + str(self.y) + ">"

ZeroVector 	= vec()
XAxisVector	= vec(1,0)
YAxisVector	= vec(0,1)

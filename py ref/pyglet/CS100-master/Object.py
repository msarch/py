
'''

	Project:	CS100
	Title:		Object

	Author:		John Mooney
	Date:		10/24/2012

	Description:
		A custom object super-class that accepts a dictionary list as an init parameter
'''

class Object(object):

	#-----------------------------------------------#
	#		Wrapper for passing kwArgs to super()	#
	#-----------------------------------------------#
	
	def __init__(self, **kwArgs):
		super().__init__()
		self.__initP__(**kwArgs)
		self.__initC__(**kwArgs)
		
	''''''''''''''''''''''''''''''''''''''
	
	#	Initalizes Variables to default values
	#		- Creates all parent-variables before child-variables 
	def __initP__(self, **kwArgs):
		pass
		
	#	Sets parent variable data utilizing personal-variables within children		#
	#		- Creates all child-variables before parent-variables
	def __initC__(self, **kwArgs):
		pass

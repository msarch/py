
'''

	Project:	CS100
	Title:		Resource

	Author:		John Mooney
	Date:		4/20/2013

	Description:
		A resource within the game
'''

# Imports
from Object import Object


#-------------------------------------------------#

class Resource(Object):
	
	def __init__(self, filename, **kwArgs):
		self._filename = filename
		super().__init__(**kwArgs)
		
	def __initC__(self, **kwArgs):
		self._load(self._filename)
		super().__initC__(**kwArgs)
		
	def _load(self):
		raise NotImplementedError

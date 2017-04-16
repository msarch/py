
'''

	Author: John Mooney
	Date:	4/8/2013
	
	Description:
		Resource Manager - Handles resource management within CS100
			- Maintains referential integrity
			- Ensures 1 allocated resource in memory
			- Provides pre, post initialization and custom resource loading
	
	Refactoring:
			- Consider creating a FileSystem manager which registers file-types and manages file paths
'''

'''		
		Manager must load a resource via it's constructor. Constructor may be passed as a parameter, aka 'user tells', 
			or may be registered into the manager with file-type associations.
			
		Consider Asynchronous IO with a "Resource Wrapper" class, that protects a resource attribute until its asynchronous load
		is complete. It can be returned within the request and parsed for access to the final resource Object
'''


# Imports
from Object import Object
import os
	

#------------------------------------------#

class ResourceManager(Object):

	activeManager = None
	
	def __init__(self, dataDirectory, **kwArgs):
		super().__init__(**kwArgs)
		self._dataDirectory = dataDirectory
		
		
	def __initP__(self, **kwArgs):
		super().__initP__(**kwArgs)
		
		self._resources = {}
		self._resourceGroups = {}
		self._resourceGroupStack = []
		self._residentResourceGroups = []
		
		self._registeredPaths = {}
		self._registeredBuilders = {}
		self._registeredResourceGroups = {}
		
		
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	@classmethod
	def getRM(cls):
		return cls.activeManager
		

	''''''''''''''''''''''''''''''''''''''''''''''''
	
	#	request(self, resourceID)
	#		- Object-level resource access
	def request(self, resId, builder=None):
		try:
			return self._resources[resId]
		except KeyError:
			filename, ext = self._getPath(resId)
			resGroups = self._getApplicableGroups(ext)
			resourceHandle = self._loadResource(filename, ext, builder)
			
			for group in resGroups:
				group.addResource(resId)
			
			self._resources[resId] = resourceHandle
			return resourceHandle
			

	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def pushGroup(self, group):
		if isinstance(group, str):
			self.pushGroup(self.createGroup(groupName = group))
		else:
			self._resourceGroupStack.append(group)
			self._residentResourceGroups.append(group.id)
	def popGroup(self):
		self._residentResourceGroups.remove((self._resourceGroupStack.pop()).id)
	
	
	def createGroup(self, groupName):
		if groupName in self._resourceGroups:
			raise ValueError("Resource Groups Must Have Unique Name Identifier")
		else:
			rg = ResourceGroup(groupName)
			self._resourceGroups[groupName] = rg
			return rg
			
			
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def _getPath(self, resId):
		root, ext = os.path.splitext(resId)
		fileDirectory = ""
		try:
			fileDirectory = self._registeredPaths[ext]
		except KeyError:
			pass
			
		return os.path.join(self._dataDirectory, fileDirectory, resId), ext
		
		
	def _getApplicableGroups(self, ext):
		try:
			return self._registeredResourceGroups[ext] + ([self._resourceGroupStack[-1]] if self._resourceGroupStack else [])
		except KeyError:
			return [self._resourceGroupStack[-1]] if self._resourceGroupStack else []
	
	def _loadResource(self, filename, ext, builder):
		if not builder:
			try:
				builder = self._registeredBuilders[ext]
			except KeyError:
				raise ValueError("Unrecognized Resource File Extension " + ext)
		
		res = builder(filename)
		return res
			
	
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def registerExtension(self, ext, path, groupNames, builder):
		self._registeredPaths[ext] = path
		self._registeredBuilders[ext] = builder
		
		rGroups = []
		for groupName in groupNames:
			rGroup = None
			
			try:
				rGroup = self._resourceGroups[groupName]
			except KeyError:
				rGroup = self.createGroup(groupName)			
			rGroups.append(rGroup)
		self._registeredResourceGroups[ext] = rGroups
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def debugDisplay(self):
		print("Resource Manager...")
		
		print("\n\tResources: ")
		for rId, r in self._resources.items():
			print("\t\t" + rId + " - " + str(type(r)))
		
		print("\n\tResource Groups: ")
		for rgId, rg in self._resourceGroups.items():
			print("\t\t" + rgId + " - " + ("R" if rgId in self._residentResourceGroups else ""))
			for rsId in rg._resourceIds:
				print("\t\t\t" + rsId)

				
#-------------------------------------------#
	
class ResourceGroup(Object):

	def __init__(self, id, **kwArgs):
		self.id = id
		super().__init__(**kwArgs)

	def __initP__(self, **kwArgs):
		super().__initP__(**kwArgs)
		self._resourceIds = []


	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def addResource(self, resId):
		self._resourceIds.append(resId)
	def removeResource(self, resId):
		self._resourceIds.remove(resId)
	

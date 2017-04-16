
'''

	Project:	CS100
	Title:		Animation

	Author:		John Mooney
	Date:		4/7/2013

	Description:
		An animation:
			- A series of image regions and timing information
'''


# Imports
from Object import Object
from Resource import Resource
from ResourceManager import ResourceManager

import re


#-----------------------------------------------#

class Animation(Resource):

	def __initC__(self, **kwArgs):
		self._frames = []
		super().__initC__(**kwArgs)
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def _load(self, filename):
		with open(filename, 'r') as of:
			lines = of.readlines()
		
		#	Remove Comments/Blank Lines
		lines = self._removeIgnored(lines)
		
		#	Read the File
		self._readMetaData(lines)
		self._readAnimData(lines)

		
	''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def getFrame(self, index):
		return self._frames[index]
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def _removeIgnored(self, lines):
		newLines = []
		for line in lines:
			if '#' in line:
				line = line.split('#')[0]
			line = line.rstrip()
			if line:
				newLines.append(line)
		return newLines
	
	
	def _readMetaData(self, lines):
		if lines[0] != "Meta:":
			raise IOError("Invalid Animation File. Expected 'Meta:'\tActual: " + lines[0])
	
	def _readAnimData(self, lines):
		try:
			activeImage	= None
			dataIndex 	= lines.index("Data:")
			
			lineNum	= dataIndex
			for line in lines[dataIndex+1:]:
				indentation = line.count("\t")
				line = line.lstrip()
				
				if indentation==1:
					activeImage = self._readImage(line)
				elif indentation==2:
					self._readFrame(line, activeImage)
				else:
					raise IOError("Invalid Animation File. Invalid Indentation at Line " + line)
					
				lineNum += 1
				
		except ValueError:
			raise IOError("Invalid Animation File. Expected 'Data:' Not Found")
		except IndexError:
			raise IOError("Invalid Data Section. Expected 'Data:\n\t'")
		except IOError as e:
			raise IOError(str(e) + " : " + line)
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def _readImage(self, line):
		rm = ResourceManager.getRM()
		image = rm.request(resId = line)
		return image
		
	def _readFrame(self, line, activeImage):
		frameLineRegex = "^(\d+)\s+-\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)(?:\s+:\s+(\d+.?\d*)([fms]))?"
		
		#	Check Match
		frameLineTokens = re.search(frameLineRegex, line)
		if not frameLineTokens:
			raise IOError("Invalid Animation File. See Frame-Data Format")
			
		#	Read Data
		frameIndex = frameLineTokens.group(1)
		xStart = frameLineTokens.group(2);		yStart = frameLineTokens.group(3)
		width  = frameLineTokens.group(4);		height = frameLineTokens.group(5)
		
		disptime = None;	units = None;
		try:
			disptime = float(frameLineTokens.group(6));	units = frameLineTokens.group(7)
		except IndexError:
			pass
		
		#	Create the Frame
		imgReg = activeImage.get_region(int(xStart), int(yStart), int(width), int(height))
		self._frames.insert(int(frameIndex), AnimationFrame(imgReg, disptime, units))
		
		
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def getFrameCount(self):
		return len(self._frames)
		
		
#-----------------------------------------------#

class AnimationFrame(Object):
	
	def __init__(self, image, time, units, **kwArgs):
		super().__init__(**kwArgs)
		
		self._image = image
		self._disptime = time
		self._timeUnits = units
	
	
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def getUnits(self):
		return self._timeUnits
	def getTime(self):
		return self._disptime
	def getImage(self):
		return self._image
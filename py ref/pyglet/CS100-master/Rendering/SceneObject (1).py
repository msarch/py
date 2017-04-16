
'''

	Project:	CS100
	Title:		SceneObject

	Author:		John Mooney
	Date:		2/27/2013

	Description:
		Converts basic vertex data into a drawable object
'''

# Imports
import Color
from pyglet.graphics import (vertex_list_indexed, GL_LINES)


from Object import Object
from Transformable import Transformable

from tools import getDictValue


#------------------------------------------------------#

class SceneObject(Transformable):
	
	def __initP__(self, **kwArgs):
		super().__initP__(**kwArgs)
		
		self._batch = getDictValue(kwArgs, None, ['b', 'batch'])
		self._group = getDictValue(kwArgs, None, ['g', 'group'])
		
		srcData	= self._getDataFromSrc(kwArgs)
		expData	= self._getExplicitData(kwArgs)
		impData	= self._getImplicitData(kwArgs)
		
		numVerts, vertexIndices, vertexListData = self._mergeData(srcData, expData, impData, kwArgs)
		self._buildVertexList(numVerts, vertexIndices, vertexListData)
	
	def __del__(self):
		self._vertexList.delete()	
	
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''
			
	def _buildVertexList(self, nv, vis, vertexListData):
		self._numVerts = nv
		if(self._batch):
			self._vertexList = self._batch.add_indexed(nv, self._drawStyle, self._group, vis, *vertexListData)
		else:
			self._vertexList = vertex_list_indexed(nv, vis, *vertexListData)

			
	''''''''''''''''''''''''''''''''''''''''''''''''
	
	def draw(self):
		if(self._batch):
			raise Exception("Batched vertex list must be drawn through batch.draw()")
		else:
			self._vertexList.draw(self._drawStyle)
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def _getDataFromSrc(self, kwArgs):
		dataSrc = getDictValue(kwArgs, None, ['dataSrc'])
		if not dataSrc:
			return [None]*4
		
		nv, ds, vis, vld = dataSrc.getVertexData()
		return (nv, ds, vis, vld)
		
		
	def _getExplicitData(self, kwArgs):
		expSrc = getDictValue(kwArgs, None, ['ed', 'fd', 'explicitData', 'formattedData'])
		if not expSrc:
			return [None]*4
			
		nv 	= getDictValue(kwArgs, None, ['nv', 'numVerts'])
		vld = expSrc
		return (nv, None, None, vld)
		

	def _getImplicitData(self, kwArgs):
		nv 	= None
		vld = None
		vs 	= getDictValue(kwArgs, None, ['vs', 'vertices'])
		ds 	= getDictValue(kwArgs, None, ['ds', 'drawStyle'])
		vis = getDictValue(kwArgs, None, ['vis', 'vertexIndices'])
		
		if vs:
			nv = len(vs)
			
			# Convert Vertices to data
			data = []
			for v in vs:
				data.append(v.x)
				data.append(v.y)
			vld = [('v2f', data)]
		
		return [nv, ds, vis, vld]


	def _mergeData(self, src, exp, imp, kwArgs):		
		numVerts 	= self._getExclusiveValue(src[0], exp[0], imp[0])
		drawStyle 	= self._getExclusiveValue(src[1], exp[1], imp[1])
		vertIndices = self._getExclusiveValue(src[2], exp[2], imp[2], False)
		
		if not vertIndices:
			vertIndices = list(range(numVerts))
		
		dataTypes		= []
		vertexDataList 	= []
		
		self._filterData(src, dataTypes, vertexDataList)
		self._filterData(exp, dataTypes, vertexDataList)
		self._filterData(imp, dataTypes, vertexDataList)
		
		# Add Color Information
		if not 'c' in dataTypes:
			vertexDataList.append(self._getColorData(numVerts, kwArgs))
			
		self._drawStyle = drawStyle
		return numVerts, vertIndices, vertexDataList


	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''		
		
	def _filterData(self, data, dataTypes, vertexDataList):
		if not data[3]:
			return
			
		for v in data[3]:
			dataType = v[0][0]
			if not dataType in dataTypes:
				dataTypes.append(dataType)
				vertexDataList.append(v)
			
	def _getExclusiveValue(self, src, exp, imp, raiseError=True, val=0):
		if (not (src or exp or imp)) and raiseError:
			raise ValueError("No Data Source given for Scene Object")

		elif src:
			if exp or imp:
				raise ValueError("Multiple Data Sources for Scene Object")
			return src
			
		elif val==2:
			return None
			
		return self._getExclusiveValue(exp, imp, src, raiseError, val+1)

	def _getColorData(self, nv, kwArgs):
		color = getDictValue(kwArgs, Color.White, ['c', 'color'])
		colors = getDictValue(kwArgs, color*nv, ['cs', 'colors'])
		return ('c3B', colors)
		
	
	''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
	def setColor(self, color):
		self._vertexList.colors[:] = color*self._numVerts
	

#-----------------------------------------------------#

class VertexDataSource(Object):

	def __initP__(self, **kwArgs):
		super().__initP__(**kwArgs)
		
		self._vis = []
		self._drawStyle = None

	#	Returns NumVerts, drawStyle, vertexIndices, formattedData
	def getVertexData(self):
		raise NotImplementedError

		

'''

	Project:	CS100
	Title:		SceneGraph

	Author:		John Mooney
	Date:		2/27/2013

	Description:
		A SceneGraph for drawing objects
'''


# Imports
import math

from TransformationGraph import TransformationGraph
from pyglet.gl import (	glPushMatrix, glPopMatrix,
	glTranslatef, glRotatef, glScalef	)


#------------------------------------------------------#

class SceneGraph(TransformationGraph):

	def draw(self):
		self._drawNode(self._rootNode)

	def _drawNode(self, n):
		glPushMatrix()
		
		glTranslatef(n._translate.x, n._translate.y, 0.0)
		glRotatef(math.degrees(n._rotateRads), 0, 0, 1)
		glScalef(n._scale.x, n._scale.y, 1)
		
		for transformable in n._transformables:
			if transformable.isDrawn:
				transformable.draw()
					
		for child in n._children:
			self._drawNode(child)
			
		glPopMatrix()

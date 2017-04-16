
'''

	Project:	CS100
	Title:		ScenePrimitives

	Author:		John Mooney
	Date:		1/23/2013

	Description:
		Entry point for running a debug CS100 version
'''

# Imports
import pyglet
import sys
import os

from pyglet.graphics import GL_LINES


'''		Set Search Directory	'''
for root, direcs, files in os.walk(os.getcwd()):
	for direc in direcs:
		sys.path.append(os.path.join(root, direc))


# Imports
import Color

from Renderer import Renderer
from TransformationGraph import Transform

from SceneObject import SceneObject
from DiscretePrimitives import *
from Vector import vec

#-------------------------------------------------------#	

window 			= pyglet.window.Window(800, 600)
winDimensions 	= [800, 600]

rendMan = Renderer(winSize=winDimensions)
sg = rendMan.getSceneGraph()

so1 = SceneObject(t=sg.newTransform(t=vec(150,0)), vs=[vec(-100,-100), vec(100,-100), vec(100,100), vec(-100,100)], ds=GL_LINES,
	vis = (0, 1, 1, 2, 2, 3, 3, 0),	cs = Color.Purple+Color.Blue+Color.Orange+Color.Green)
so2 = SceneObject(t=so1.getTransform().createChild(), dataSrc=DiscreteRect(10, 50))
so3 = SceneObject(t=sg.newTransform(), numVerts=3, drawStyle=GL_TRIANGLES, explicitData=[('v2f/static', [-30, -30, 30, -30, 0, 30])])


def update(dt):
	so2.rotate(.005)
	
@window.event
def on_draw():
	window.clear()
	rendMan.render()

pyglet.clock.schedule(update)
pyglet.app.run()


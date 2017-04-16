
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

from Vector import vec
from Sprite import Sprite
from Renderer import Renderer
from Animation import Animation
from TransformationGraph import Transform
from ResourceManager import ResourceManager

#-------------------------------------------------------#	

window 			= pyglet.window.Window(800, 600)
winDimensions 	= [800, 600]

rendMan = Renderer(winSize=winDimensions)
Renderer.activeRenderer = rendMan

sg = rendMan.getSceneGraph()

rm = ResourceManager("Tests\\data")
ResourceManager.activeManager = rm
rm.registerExtension(".jpg", "img", ["img"], pyglet.image.load)
rm.registerExtension(".bmp", "img", ["img"], pyglet.image.load)
rm.registerExtension(".png", "img", ["img"], pyglet.image.load)
rm.registerExtension(".anim", "anim", ["anim"], Animation)

anim1 = rm.request("CharizardEvolve.anim")
anim2 = rm.request("PShip.anim")

s1 = Sprite(anim1, t=sg.newTransform())
s2 = Sprite(anim2, t=sg.newTransform(t=vec(-200,100)))

s1.setAnimation("Alternating")
s2.setAnimation("Looping")


print("")
rm.debugDisplay()
print("")


def update(dt):
	s1.update(dt)
	s2.update(dt)


	
	
@window.event
def on_draw():
	window.clear()
	rendMan.render()

pyglet.clock.schedule(update)
pyglet.app.run()


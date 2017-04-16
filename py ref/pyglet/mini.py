#!/usr/bin/env python
# pyglet version of NeHe's OpenGL lesson02
# based on the pygame+PyOpenGL conversion by Paul Furber 2001 - m@verick.co.za
# $Philip Bober 2007 pdbober@gmail.com

from pyglet.gl import *
from pyglet import window
import pyglet.clock
win = window.Window(width=640,height=480,visible=True)
glClearColor(0.0, 0.0, 0.0, 0.0)
@ win.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	glTranslatef(-1.5, 0.0, -6.0)

	glBegin(GL_TRIANGLES)
	glVertex3f(0.0, 1.0, 3.0)
	glVertex3f(-1.0, -1.0, 0)
	glVertex3f(1.0, -1.0, 0)
	glEnd()

def main():
        pyglet.app.run()
if __name__ == '__main__': main()

#!/usr/bin/env python
# pyglet version of NeHe's OpenGL lesson01
# based on the pygame+PyOpenGL conversion by Paul Furber 2001 - m@verick.co.za
# Philip Bober 2007 pdbober@gmail.com

from pyglet.gl import *
from pyglet import window

def init():
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 1.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def square ():
    glBegin(GL_QUADS)               #begin the four sided shape
    glVertex3f(-5, -0.5, 0.0)     #first corner at -0.5, -0.5
    glVertex3f(-0.5, 0.5, 0.0)      #second corner at -0.5, 0.5
    glVertex3f(0.5, 0.5, 0.0)       #third corner at 0.5, 0.5
    glVertex3f(0.5, -0.5, 0.0)      #fourth corner at 0.5, -0.5
    glEnd()

def draw():
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        square()

def main():

        win = window.Window(width=640,height=480,visible=False)

        init()

        win.set_visible()
        clock=pyglet.clock.Clock()

        while not win.has_exit:
                win.dispatch_events()

                draw()
                win.flip()
                clock.tick()


        print "fps:  %d" % clock.get_fps()

if __name__ == '__main__': main()

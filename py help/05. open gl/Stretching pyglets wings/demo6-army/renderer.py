from __future__ import division
from math import pi
from pyglet import clock
from pyglet.gl import *
from pyglet.graphics import draw
from pyglet.window import key
from keyboard import key_handlers

rad2deg = 180 / pi
clockDisplay = clock.ClockDisplay()

class Renderer(object):

    def __init__(self):
        glClearColor(0.2, 0.5, 0.0, 0)

    def on_draw(self, creatures, camera, win_width, win_height):
        glClear(GL_COLOR_BUFFER_BIT)
        camera.update_position()
        camera.focus(win_width, win_height)

        for creature in creatures:
            glPushMatrix()
            glTranslatef(creature.x, creature.y, 0)
            glRotatef(creature.angle * rad2deg, 0, 0, 1)
            creature.shape.get_batch().draw()
            glPopMatrix()

        camera.hud_mode(win_width, win_height)
        clockDisplay.draw()


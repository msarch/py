#! python -O
"""
Demo 4
A 'Creature' now stores the (x,y,angle) of a monster to be drawn on screen.
Each creature has a Shape. A shape stores a list of Primitive objects.
A Primitive - analogous to our previous 'list of arrays' - stores a
single list of vertices.

Using these we can now compose interesting shapes instead of just triangles.
"""
from __future__ import division
from math import pi
from random import uniform
from sys import stdout
from pyglet import app, clock
from pyglet.window import key, Window
from pyglet.window.key import symbol_string
from pyglet.gl import *
from camera import Camera
from data import ghost, pacman
from creature import Creature, Popup

rad2deg = 180 / pi

win = Window(fullscreen=True, visible=False)
clockDisplay = clock.ClockDisplay()
glClearColor(0.4, 0.3, 0.6, 0)
camera = Camera((0, 0), 15)

creatures = []


def render(shape):
    for primitive in shape.primitives:
        glColor3ub(*primitive.color)
        glBegin(primitive.primtype)
        for vert in primitive.verts:
            glVertex2f(*vert)
        glEnd()


@win.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    camera.update()
    camera.focus(win.width, win.height)

    for creature in creatures:

        glPushMatrix()
        glTranslatef(creature.x, creature.y, 0)
        glRotatef(creature.angle * rad2deg, 0, 0, 1)

        render(creature.shape)

        glPopMatrix()

    camera.hud_mode(win.width, win.height)
    clockDisplay.draw()


@win.event
def on_key_press(symbol, modifiers):
    handler = key_handlers.get(symbol, lambda: None)
    handler()


def update(dt):
    for creature in creatures:
        creature.update(dt)


def create_popup():
    creature = Popup(ghost, (uniform(-14, +14), -19))
    creatures.append(creature)


def create_chase():
    p = Creature(pacman, (+30, 0))
    p.dx = -0.4
    creatures.append(p)
    g = Creature(ghost, (+50, 0))
    g.dx = -0.4
    creatures.append(g)


key_handlers = {
    key.ESCAPE: lambda: win.close(),
    key.PAGEUP: lambda: camera.zoom(2),
    key.PAGEDOWN: lambda: camera.zoom(0.5),
    key.LEFT: lambda: camera.pan(camera.scale, -pi/2),
    key.RIGHT: lambda: camera.pan(camera.scale, +pi/2),
    key.DOWN: lambda: camera.pan(camera.scale, pi),
    key.UP: lambda: camera.pan(camera.scale, 0),
    key.COMMA: lambda: camera.tilt(-1),
    key.PERIOD: lambda: camera.tilt(+1),
    key._1: create_popup,
    key._2: create_chase,
}

clock.schedule(update)

print "keys to try:", [symbol_string(k) for k in key_handlers.keys()]
stdout.flush()
win.set_visible()
app.run()


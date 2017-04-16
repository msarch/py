#! python -O
"""
Demo3
A single vertlist can be drawn in more than one place at once.
Entities reference a vertlist, and maintain their own x,y,angle.
"""
from __future__ import division
from math import cos, pi, sin, sqrt
from random import gauss, uniform
from sys import stdout
from pyglet import app, clock, image
from pyglet.window import key, Window
from pyglet.window.key import symbol_string
from pyglet.gl import *
from camera import Camera
from entity import Entity

rad2deg = 180 / pi

verts = [
    ((000, 255, 000), (+0, -5)),
    ((000, 000, 255), (-8, +5)),
    ((255, 000, 000), (+8, +5)),
]

def create_flock(num_ents):
    entities = []
    max_radius = 400
    min_radius = 40
    for idx in range(num_ents):
        length = sqrt(uniform(0, max_radius - min_radius) ** 2) + min_radius
        angle = uniform(-pi, +pi)
        x = length * sin(angle)
        y = length * cos(angle)
        ent = Entity(verts, (x, y), uniform(-pi, +pi))
        entities.append(ent)
    ent = Entity(verts, (0, 0))
    entities.append(ent)
    return entities

entities = create_flock(800)

win = Window(fullscreen=True, visible=False)
clockDisplay = clock.ClockDisplay()
glClearColor(0.4, 0.5, 0.3, 0)
camera = Camera((0, 0), 5)

@win.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    camera.update()
    camera.focus(win.width, win.height)

    for entity in entities:

        glPushMatrix()
        glTranslatef(entity.x, entity.y, 0)
        glRotatef(entity.angle * rad2deg, 0, 0, 1)

        glBegin(GL_TRIANGLES)
        for color, position in entity.verts:
            glColor3ub(*color)
            glVertex2f(*position)
        glEnd()

        glPopMatrix()

    camera.hud_mode(win.width, win.height)
    clockDisplay.draw()

def update(dt):
    for idx, entity in enumerate(entities):
        entity.angle += ((entity.x) + abs(entity.y)) / 10000
        entity.x += sin(entity.angle) / (1+idx) * 10
        entity.y -= cos(entity.angle) / (1+idx) * 10
    camera.zoom(1.008)

clock.schedule(update) # triggers on_draw event when done

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
}

@win.event
def on_key_press(symbol, modifiers):
    handler = key_handlers.get(symbol, lambda: None)
    handler()

print "keys to try:", [symbol_string(k) for k in key_handlers.keys()]
stdout.flush()
win.set_visible()
app.run()


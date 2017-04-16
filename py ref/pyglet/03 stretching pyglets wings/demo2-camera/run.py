#! python -O
"""
Demo2
Add a moveable/zoomable camera.
"""
from __future__ import division
from sys import stdout
from math import pi
from pyglet import app, clock
from pyglet.window import key, Window
from pyglet.window.key import symbol_string
from pyglet.gl import *
from camera import Camera

win = Window(fullscreen=True, visible=False)
clockDisplay = clock.ClockDisplay()
glClearColor(0.4, 0.2, 0.3, 0)
camera = Camera((0, 0), 5)

verts = [
    ((255, 000, 000), (+5, +4)),
    ((000, 255, 000), (+0, -4)),
    ((000, 000, 255), (-5, +4)),
]

@win.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    camera.update()
    camera.focus(win.width, win.height)

    glBegin(GL_TRIANGLES)
    for color, position in verts:
        glColor3ub(*color)
        glVertex2f(*position)
    glEnd()

    camera.hud_mode(win.width, win.height)
    clockDisplay.draw()

# on_draw is triggered after all events by default. This 'null' event
# is scheduled just to force a screen redraw for every frame
clock.schedule(lambda _: None)

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


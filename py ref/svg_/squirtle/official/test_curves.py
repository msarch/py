import pyglet
from pyglet.gl import *

import sys

import squirtle

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "svgs/zapf.svgz"

w = pyglet.window.Window(800, 600)
keys = pyglet.window.key.KeyStateHandler()
w.push_handlers(keys)

glClearColor(1,1,1,1)

squirtle.setup_gl()

s = squirtle.SVG(filename)
s.anchor_x, s.anchor_y = s.width/2, s.height/2

zoom = 1
angle = 0
draw_x = 400
draw_y = 300

def tick(dt):
    global zoom, angle, draw_x, draw_y
    if keys[pyglet.window.key.W]:
        draw_y -= 8
    elif keys[pyglet.window.key.S]:
        draw_y += 8
    elif keys[pyglet.window.key.D]:
        draw_x -= 8
    elif keys[pyglet.window.key.A]:
        draw_x += 8
    elif keys[pyglet.window.key.UP]:
        zoom *= 1.1
    elif keys[pyglet.window.key.DOWN]:
        zoom /= 1.1
    elif keys[pyglet.window.key.LEFT]:
        angle -= 8
    elif keys[pyglet.window.key.RIGHT]:
        angle += 8

pyglet.clock.schedule_interval(tick, 1/60.0)


@w.event
def on_draw():
    w.clear()
    s.draw(draw_x, draw_y, scale=zoom, angle=angle)

pyglet.app.run()

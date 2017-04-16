#! python -O
"""
Demo 5
Keys switch between rendering using:
    1 - pyglet.gl.glvertex
    2 - pyglet.graphics.draw
    3 - pyglet.graphics.vertex_list
    4 - pyglet.graphics.batch
Options 2 and 3 are actually slower than mode 1. I don't know why. It is
probable that vertex_lists would be faster than glVertex calls for larger
arrays of vertices (eg. thousands or tens of thousands of vertices per
primitive) Fortunately, mode 4 manages to claw back some ground and is faster
than mode 1. For a good throughput demo using vertex lists, see demos 7 and 8
instead, where I dug out some old code of mine that uses openGL vertex lists,
and they are fast.
"""
from random import randint, uniform
from sys import stdout
from pyglet import app, clock
from pyglet.window import key, Window
from pyglet.window.key import symbol_string
from camera import Camera
from data import blue_ghost, orange_ghost, pacman, pink_ghost, red_ghost
from creature import Creature
from keyboard import on_key_press, key_handlers
from renderer import Renderer

win = Window(fullscreen=True, visible=False)
camera = Camera((0, 0), 70)
renderer = Renderer()

def make_army(size, menagerie):
    army = []
    for col in range(size):
        for row in range(size):
            creature_type = menagerie[randint(0, len(menagerie)-1)]
            x = (col+0.5)*16 - size * 8
            y = (row+0.5)*16 - size * 8
            creature = Creature(creature_type, (x, y))
            creature.da = uniform(-0.1, +0.1)
            creature.velocity = uniform(0, +0.5)
            army.append(creature)
    return army

creatures = make_army(12, [blue_ghost, orange_ghost, pacman, pink_ghost, red_ghost])

def update(dt):
    for creature in creatures:
        creature.update(dt)

clock.schedule(update)

key_handlers[key.ESCAPE] = win.close
win.on_draw = lambda: renderer.on_draw(creatures, camera, win.width, win.height)
win.on_key_press = on_key_press

print "keys to try:", [symbol_string(k) for k in key_handlers.keys()]
stdout.flush()
win.set_visible()
app.run()


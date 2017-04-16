#! python -O
"""
Demo 6
Render several armies of ghosts. Each army contains many ghosts, which are all
drawn in a single batch.draw() call.
"""
from math import pi
from random import randint, uniform
from sys import stdout
from pyglet import app, clock
from pyglet.window import key, Window
from pyglet.window.key import symbol_string
from army import Army, rand_point
from camera import Camera
from data import all_ghosts, pacman
from creature import Creature
from keyboard import on_key_press, key_handlers
from renderer import Renderer

win = Window(fullscreen=True, visible=False)
camera = Camera((0, 0), 10)
renderer = Renderer()

army_shape = Army.MakeShape(400, 1500, all_ghosts)
armies = []
for i in range(20, 0, -1):
    army = Creature(army_shape, rand_point(500), uniform(-pi, pi))
    army.dx = uniform(-0.4, +0.4)
    army.dy = uniform(-0.4, +0.4)
    armies.append(army)

def update(dt):
    for army in armies:
        army.update(dt)
    camera.zoom(1.003)

clock.schedule(update)

key_handlers[key.ESCAPE] = win.close
win.on_draw = lambda: renderer.on_draw(armies, camera, win.width, win.height)
win.on_key_press = on_key_press

print "keys to try:", [symbol_string(k) for k in key_handlers.keys()]
stdout.flush()
win.set_visible()
app.run()


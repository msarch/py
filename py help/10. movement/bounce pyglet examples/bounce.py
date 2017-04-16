#!/usr/bin/env python

import os
import random
import sys

from pyglet.gl import *
import pyglet
from pyglet.window import key

window = pyglet.window.Window(640, 480)
BALL_IMAGE = 'star.png'
balls_batch = pyglet.graphics.Batch()
balls = []
label = pyglet.text.Label('Press space to add a ball, backspace to remove',
                          font_size=14,
                          x=window.width // 2, y=10,
                          anchor_x='center')

class Ball(pyglet.sprite.Sprite):
    ball_image = pyglet.resource.image(BALL_IMAGE)
    width = ball_image.width
    height = ball_image.height

    def __init__(self):
        x = window.width/2
        y = window.height/2

        super(Ball, self).__init__(self.ball_image, x, y, batch=balls_batch)

        self.dx = (random.random() - 0.5) * 1000
        self.dy = (random.random() - 0.5) * 1000

    def update(self, dt):
        if self.x <= 0 or self.x + self.width >= window.width:
            self.dx *= -1
        if self.y <= 0 or self.y + self.height >= window.height:
            self.dy *= -1
        self.x += self.dx * dt
        self.y += self.dy * dt

        self.x = min(max(self.x, 0), window.width - self.width)
        self.y = min(max(self.y, 0), window.height - self.height)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        balls.append(Ball())
    elif symbol == key.BACKSPACE:
        if balls:
            del balls[-1]
    elif symbol == key.ESCAPE:
        window.has_exit = True

@window.event
def on_draw():
    window.clear()
    balls_batch.draw()
    label.draw()

def update(dt):
    for ball in balls:
        ball.update(dt)
pyglet.clock.schedule_interval(update, 1.)




pyglet.app.run()

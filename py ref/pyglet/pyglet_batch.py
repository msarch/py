#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# pyglet_batch.py
# what : pyglet batch example



import pyglet

window = pyglet.window.Window()

batch = pyglet.graphics.Batch()

x = 10
y = 10
width =150
height = 150
color = 127, 127, 0, 127

batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                    [0, 1, 2, 1, 2, 3],
                    ('v2i', (x, y,
                             x + width, y,
                             x, y + height,
                             x + width,
                             y + height)),
                    ('c4B', tuple(color * 4)))

def sq_update(dt):
    global x
    x+= 1
    pass

@window.event
def on_draw():
	window.clear()
	batch.draw()

# schedule the update function, 60 times per second
pyglet.clock.schedule_interval(sq_update, 1.0/60.0)
pyglet.app.run()
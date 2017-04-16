
#
# Circle1D: A lame 2D "Physics" Engine <http://thp.io/2013/circle1d/>
# Copyright (c) 2013, Thomas Perl.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import print_function

import pyglet
import math

import model
import content

window = pyglet.window.Window(width=1280, height=760)

class Renderer:
    def __init__(self, window, step_size=5):
        self.window = window
        def generate_vertices():
            for i in range(0, 361, step_size):
                angle = i*math.pi/180
                yield math.cos(angle)
                yield math.sin(angle)
        circle_data = list(generate_vertices())
        self.vertex_list = pyglet.graphics.vertex_list(len(circle_data)/2,
                ('v2f', circle_data))

    def draw_circle(self, pos, radius):
        pos = model.Vec2(pos.x, self.window.height-pos.y)
        pyglet.gl.glColor3f(1., 0., 0.)
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(pos.x, pos.y, 0)
        pyglet.gl.glScalef(radius, radius, 1)
        self.vertex_list.draw(pyglet.gl.GL_LINE_STRIP)
        pyglet.gl.glPopMatrix()

    def draw_line(self, a, b):
        a = model.Vec2(a.x, self.window.height-a.y)
        b = model.Vec2(b.x, self.window.height-b.y)
        pyglet.gl.glColor3f(0., 1., 0.)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                ('v2f', (a.x, a.y, b.x, b.y)))

renderer = Renderer(window)

scene = model.Scene(renderer)
content.scene_square(scene)
content.scene_floor(scene)
content.scene_rubberband(scene)
content.scene_bubbles(scene)

# Simulation events happen every 20 ms
pyglet.clock.schedule_interval(lambda dt: scene.simulate(), .02)

# FPS debug output happens every second
pyglet.clock.schedule_interval(lambda dt: print('FPS: %.2f' % pyglet.clock.get_fps()), 1.)

@window.event
def on_draw():
    pyglet.clock.tick()
    window.clear()
    scene.render()

@window.event
def on_mouse_press(x, y, button, modifiers):
    scene.handle(model.Event(model.Event.PRESS, model.Vec2(x, window.height - y)))

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    scene.handle(model.Event(model.Event.DRAG, model.Vec2(dx, -dy)))

@window.event
def on_mouse_release(x, y, button, modifiers):
    scene.handle(model.Event(model.Event.RELEASE, model.Vec2(x, window.height - y)))

pyglet.app.run()


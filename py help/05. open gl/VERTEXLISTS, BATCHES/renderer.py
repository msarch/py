from __future__ import division
from math import pi
from pyglet import clock
from pyglet.gl import *
from pyglet.graphics import draw
from pyglet.window import key
from keyboard import key_handlers

rad2deg = 180 / pi
clockDisplay = clock.ClockDisplay()

class RenderMode(object):
    GLVERTEX = 0
    DRAW = 1
    VERTEXLIST = 2
    BATCH = 3

class Renderer(object):

    def __init__(self):
        self.rendermode = RenderMode.BATCH
        self.set_key_handlers()
        glClearColor(0.3, 0.7, 0.4, 0)

    def set_key_handlers(self):
        key_handlers.update({
            key._1: lambda: self.set_rendermode(RenderMode.GLVERTEX),
            key._2: lambda: self.set_rendermode(RenderMode.DRAW),
            key._3: lambda: self.set_rendermode(RenderMode.VERTEXLIST),
            key._4: lambda: self.set_rendermode(RenderMode.BATCH),
        })

    def set_rendermode(self, newmode):
        self.rendermode = newmode

    def on_draw(self, creatures, camera, win_width, win_height):
        glClear(GL_COLOR_BUFFER_BIT)
        camera.update_position()
        camera.focus(win_width, win_height)

        for creature in creatures:

            glPushMatrix()
            glTranslatef(creature.x, creature.y, 0)
            glRotatef(creature.angle * rad2deg, 0, 0, 1)

            if self.rendermode == RenderMode.BATCH:
                batch = creature.shape.get_batch()
                batch.draw()
            else:

                for primitive in creature.shape.primitives:

                    if self.rendermode == RenderMode.VERTEXLIST:

                        vertexlist = primitive.get_vertexlist()
                        vertexlist.draw(primitive.primtype)

                    elif self.rendermode == RenderMode.DRAW:

                        flatverts = primitive.get_flat_verts()
                        numverts = int(len(flatverts) / 2)
                        draw(
                            numverts,
                            primitive.primtype,
                            ('v2f/static', flatverts),
                            ('c3B/static', primitive.color * numverts),
                        )

                    elif self.rendermode == RenderMode.GLVERTEX:

                        glColor3ub(*primitive.color)
                        glBegin(primitive.primtype)
                        for vert in primitive.verts:
                            glVertex2f(*vert)
                        glEnd()

            glPopMatrix()

        camera.hud_mode(win_width, win_height)
        clockDisplay.draw()


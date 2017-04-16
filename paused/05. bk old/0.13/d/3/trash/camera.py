#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: camera :: rev 13-d3 :: 10.2013 :: msarch@free.fr

"""
Camera tracks a position, orientation and zoom level, and applies openGL
transforms so that subsequent renders are drawn at the correct place, size
and orientation on screen
"""
from __future__ import division
from math import sin, cos

from pyglet.gl import (
    glLoadIdentity, glMatrixMode, gluLookAt, gluOrtho2D,
    GL_MODELVIEW, GL_PROJECTION,
)


class Camera(object):

    def __init__(self, xmax, ymax, scale=1.0, angle=0.0):
        self.x, self.y = xmax*0.5, ymax*0.5
        self.aspect = self.x/self.y
        self.scale = scale
        self.angle = angle
        # set target to same pos, angle and scale
        self.target_x, self.target_y = self.x, self.y
        self.target_scale = self.scale
        self.target_angle = self.angle

    def zoom(self, factor):
        self.target_scale *= factor

    def pan(self, length, angle):
        self.target_x += length * sin(angle + self.angle)
        self.target_y += length * cos(angle + self.angle)

    def tilt(self, angle):
        self.target_angle += angle


    def update(self):
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1
        self.scale += (self.target_scale - self.scale) * 0.1
        self.angle += (self.target_angle - self.angle) * 0.1

        "Set projection and modelview matrices ready for rendering"

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluOrtho2D(
            -self.scale * self.aspect,
            +self.scale * self.aspect,
            -self.scale,
            +self.scale)

        # Set modelview matrix to move, scale & rotate to camera position"
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            self.x, self.y, +1.0,
            self.x, self.y, -1.0,
            sin(self.angle), cos(self.angle), 0.0)
        print 'gluLookAt:', self.x,self.y, self.angle


    def hud_mode(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

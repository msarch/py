#!/usr/bin/python # -*- coding: iso-8859-1 -*-
# msarch@free.fr
#       jan 2015
#        rev 113

#--- IMPORTS ------------------------------------------------------------------
from math import pi, sin, cos
from pyglet.gl import GL_TRIANGLE_STRIP, GL_LINE_STRIP
from shape import Shape

##--- CONSTANTS AND VARIABLES -------------------------------------------------

#--- COMMON SHAPES (CIRCLES) --------------------------------------------------

class Circle(Shape):
    """
    Circle, outline only
    """
    def build(self):
        self.primtype = GL_LINE_STRIP
        # nov = number of divisions per ∏ rads (half the circle)
        # with vertices numbered like a clock,  GL_TRIANGLE_STRIP order is:
        # 11, 12, 10, 1, 9, 2, 8, 3, 7, 4, 6, 5
        stepangle = pi/(int(self.radius/5)+3)
        phi=0
        self.verts.append((0, self.radius))
        while phi<pi:
            x = self.radius * sin(phi)
            y = self.radius * cos(phi)
            self.verts.append((x, y))
            phi += stepangle
        self.verts.append((0,-self.radius))  # add right side vertex
        #mirrored_verts=[]
        for vert in reversed(self.verts):
	#    mirrored_verts.append((-vert[0],vert[1]))
        # verts.extend(mirrored_verts)
            self.verts.append((-vert[0],vert[1]))


circle=Circle

#!/usr/bin/python # -*- coding: iso-8859-1 -*-
# msarch@free.fr
#       dec 2014
#        rev 113

#--- IMPORTS ------------------------------------------------------------------
from math import pi, sin, cos
from pyglet.gl import GL_TRIANGLE_STRIP, GL_LINE_STRIP
from shapes import Shape
from utils.cfg import red  # all colors

##--- CONSTANTS AND VARIABLES -------------------------------------------------

#--- COMPOSITE SHAPES (Groups) ------------------------------------------------
class Baton(Shape):
    """
    Group : Rouned End Segment, filled with a single color
    """
    def build(self):
        if not hasattr(self,'color'):
            self.color = red
        self.verts = self.get_verts()
        self.primtype = GL_TRIANGLE_STRIP

    def get_verts(self):
        # nov = number of divisions per ∏ rads (half the circle)
        # with vertices numbered like a clock,  GL_TRIANGLE_STRIP order is:
        # 11, 12, 10, 1, 9, 2, 8, 3, 7, 4, 6, 5
        verts=[]
        stepangle = pi/(int(self.radius/5)+3)
        phi=0
        verts.append((0, self.radius))
        while phi<pi:
            x = self.radius * sin(phi)
            y = self.radius * cos(phi)
            verts.append((x, y))
            verts.append((x, -y))
            phi += stepangle
        verts.append((0,-self.radius))  # add right side vertex
        mirrored_verts=[]
        for vert in reversed(verts):
	    mirrored_verts.append((-vert[0],vert[1]))
        verts.extend(mirrored_verts)

        return(verts)



#!/usr/bin/python
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus :: rev 13-d2 :: 10.2013 :: msarch@free.fr

##--- IMPORTS -----------------------------------------------------------------

from pyglet.gl import *
import pyglet

##--- CONSTANTS AND VARIABLES -------------------------------------------------

##--- CLASSES -----------------------------------------------------------------

class Shape(object):

    def draw(self,position):
        """ draw to screen,
        should be defined by each subclass
        """
        pass

#--- COLOR MIXIN -------------------------------------------------------------------------------------
# Drawing commands like rect() have optional parameters fill and stroke to set the color directly.

def color_mixin(**kwargs):
    fill        = kwargs.get("fill", _fill)
    stroke      = kwargs.get("stroke", _stroke)
    strokewidth = kwargs.get("strokewidth", _strokewidth)
    strokestyle = kwargs.get("strokestyle", _strokestyle)
    return (fill, stroke, strokewidth, strokestyle)

#--- POINT -------------------------------------------------------------------------------------------

class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def _get_xy(self):
        return (self.x, self.y)
    def _set_xy(self, (x,y)):
        self.x = x
        self.y = y

    xy = property(_get_xy, _set_xy)

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return "Point(x=%.1f, y=%.1f)" % (self.x, self.y)

    def __eq__(self, pt):
        if not isinstance(pt, Point): return False
        return self.x == pt.x \
           and self.y == pt.y

    def __ne__(self, pt):
        return not self.__eq__(pt)

#--- RECT -------------------------------------------------------------------------------------------

class Rect(Shape):
    """ rectangle is a shape attribute defined by :
            initial x,y axis, width, height as args
            initial x,y speed,color are kwargs
            AABB
    """
    def __init__(self,width=300, height=100):
        # self vertex list:
        #                             centroid,     [0]
        #                             bottom left,  [1]
        #                             bottom right, [2]
        #                             top right,    [3]
        #                             top left      [4]
        self.width=width
        self.height=height
        self.vtx=[[-self.width*0.5,-self.height*0.5],\
                        [self.width*0.5,-self.height*0.5],\
                        [self.width*0.5,self.height*0.5],\
                        [-self.width*0.5,self.height*0.5],]


    def draw(self):
        """ Draws the rectangle with the bottom left corner at x, y.
        The current stroke, strokewidth and fill color are applied.
        """
        glBegin(GL_QUADS)
        glVertex3f(self.vtx[0][0], self.vtx[0][1], 0.0)  # bottom left
        glVertex3f(self.vtx[1][0], self.vtx[1][1], 0.0)  # bottom right
        glVertex3f(self.vtx[2][0], self.vtx[2][1], 0.0)  # top right
        glVertex3f(self.vtx[3][0], self.vtx[3][1], 0.0)  # top left
        glEnd()



# from NODEBOXGL

#=====================================================================================================

#--- DRAWING PRIMITIVES ------------------------------------------------------------------------------
# Drawing primitives: Point, line, rect, ellipse, arrow. star.
# The fill and stroke are two different shapes put on top of each other.


def line(x0, y0, x1, y1, **kwargs):
    """ Draws a straight line from x0, y0 to x1, y1 with the current stroke color and strokewidth.
    """
    fill, stroke, strokewidth, strokestyle = color_mixin(**kwargs)
    if stroke is not None and strokewidth > 0:
        glColor4f(stroke[0], stroke[1], stroke[2], stroke[3] * _alpha)
        glLineWidth(strokewidth)
        glLineDash(strokestyle)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x0, y0)
        glVertex2f(x1, y1)
        glEnd()

def rect(x, y, width, height, **kwargs):
    """ Draws a rectangle with the bottom left corner at x, y.
        The current stroke, strokewidth and fill color are applied.
    """
    fill, stroke, strokewidth, strokestyle = color_mixin(**kwargs)
    for i, clr in enumerate((fill, stroke)):
        if clr is not None and (i==0 or strokewidth > 0):
            if i == 1:
                glLineWidth(strokewidth)
                glLineDash(strokestyle)
            glColor4f(clr[0], clr[1], clr[2], clr[3] * _alpha)
            # Note: this performs equally well as when using precompile().
            glBegin((GL_POLYGON, GL_LINE_LOOP)[i])
            glVertex2f(x, y)
            glVertex2f(x+width, y)
            glVertex2f(x+width, y+height)
            glVertex2f(x, y+height)
            glEnd()

def triangle(x1, y1, x2, y2, x3, y3, **kwargs):
    """ Draws the triangle created by connecting the three given points.
        The current stroke, strokewidth and fill color are applied.
    """
    fill, stroke, strokewidth, strokestyle = color_mixin(**kwargs)
    for i, clr in enumerate((fill, stroke)):
        if clr is not None and (i==0 or strokewidth > 0):
            if i == 1:
                glLineWidth(strokewidth)
                glLineDash(strokestyle)
            glColor4f(clr[0], clr[1], clr[2], clr[3] * _alpha)
            # Note: this performs equally well as when using precompile().
            glBegin((GL_POLYGON, GL_LINE_LOOP)[i])
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
            glVertex2f(x3, y3)
            glEnd()

_ellipses = {}
ELLIPSE_SEGMENTS = 50
def ellipse(x, y, width, height, segments=ELLIPSE_SEGMENTS, **kwargs):
    """ Draws an ellipse with the center located at x, y.
        The current stroke, strokewidth and fill color are applied.
    """
    if not segments in _ellipses:
        # For the given amount of line segments, calculate the ellipse once.
        # Then reuse the cached ellipse by scaling it to the desired size.
        _ellipses[segments] = []
        for mode in (GL_POLYGON, GL_LINE_LOOP):
            _ellipses[segments].append(precompile(lambda:(
                glBegin(mode),
               [glVertex2f(cos(t)/2, sin(t)/2) for t in [2*pi*i/segments for i in range(segments)]],
                glEnd()
            )))
    fill, stroke, strokewidth, strokestyle = color_mixin(**kwargs)
    for i, clr in enumerate((fill, stroke)):
        if clr is not None and (i==0 or strokewidth > 0):
            if i == 1:
                glLineWidth(strokewidth)
                glLineDash(strokestyle)
            glColor4f(clr[0], clr[1], clr[2], clr[3] * _alpha)
            glPushMatrix()
            glTranslatef(x, y, 0)
            glScalef(width, height, 1)
            glCallList(_ellipses[segments][i])
            glPopMatrix()

oval = ellipse # Backwards compatibility.

#--- COLOR PLANE -------------------------------------------------------------------------------------
# Not part of the standard API but too convenient to leave out.
def colorplane(x, y, width, height, *a):
    """ Draws a rectangle that emits a different fill color from each corner.
        An optional number of colors can be given:
        - four colors define top left, top right, bottom right and bottom left,
        - three colors define top left, top right and bottom,
        - two colors define top and bottom,
        - no colors assumes black top and white bottom gradient.
    """
    if len(a) == 2:
        # Top and bottom colors.
        clr1, clr2, clr3, clr4 = a[0], a[0], a[1], a[1]
    elif len(a) == 4:
        # Top left, top right, bottom right, bottom left.
        clr1, clr2, clr3, clr4 = a[0], a[1], a[2], a[3]
    elif len(a) == 3:
        # Top left, top right, bottom.
        clr1, clr2, clr3, clr4 = a[0], a[1], a[2], a[2]
    elif len(a) == 0:
        # Black top, white bottom.
        clr1 = clr2 = (0,0,0,1)
        clr3 = clr4 = (1,1,1,1)
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(width, height, 1)
    glBegin(GL_QUADS)
    glColor4f(clr1[0], clr1[1], clr1[2], clr1[3] * _alpha); glVertex2f(-0.0,  1.0)
    glColor4f(clr2[0], clr2[1], clr2[2], clr2[3] * _alpha); glVertex2f( 1.0,  1.0)
    glColor4f(clr3[0], clr3[1], clr3[2], clr3[3] * _alpha); glVertex2f( 1.0, -0.0)
    glColor4f(clr4[0], clr4[1], clr4[2], clr4[3] * _alpha); glVertex2f(-0.0, -0.0)
    glEnd()
    glPopMatrix()


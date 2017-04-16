#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# who : michel serratrice / msarch@free.fr
# when : 04.2013
# what : elements géometriques 2d, fonctions graphiques associées

# kbw r0.9

##--- COMMENTS ----------------------------------------------------------------
# some code from https://github.com/the-swerve/langtonsant
# some code inspired by nodeboxGL
# ...
# note on transform() method :
# the 3x3 affine matrix multiplication with a vertex is :
#    [x']   [m0 m1 m2]   [x]
#    [y'] = [m3 m4 m5] * [y]
#    [z']   [m6 m7 m8]   [1]
# but z and z' always = 1, thus we will only (x',y') :
# x',y' = (m[0]*x+m[1]*y+m[2], m[3]*x+m[4]*y+m[5])
# ...


##--- CONSTANTS AND VARIABLES -------------------------------------------------
pt=5 # point display size
grobs=[] #list of all groms created

##--- IMPORTS -----------------------------------------------------------------
from pyglet.gl import *
from flatmath import *

##--- CLASSES & FUNCTIONS -----------------------------------------------------
##--- Grob ------------------------------------------------------------------
class Grob(object):
    """ 2d graphic geometrical object
    has : position, matrix of transformation
    may also have : other geometrical properties ass needed
    in the future : fill and stroke color info, stroke width
    """

    @property
    def type(self):
        return (self.__class__)

    @property
    def M(self):
        return (self._M)

    @M.setter
    def M(self,matrix):
        self._M = matrix

    @property
    def color(self):
        return (self._color)

    @color.setter
    def color(self,c):
        self._color = c

    def once_transform(self,M):
        """ applies the PROVIDED matrix M transformation to all vertex.
        """
        for index, vtx in enumerate(self.v):
            self.v[index] = [M[0]*vtx[0]+M[1]*vtx[1]+M[2],\
                             M[3]*vtx[0]+M[4]*vtx[1]+M[5]]

    def transform(self):
        """ applies OWN's CURRENT matrix transformation
        to all transformable vertex, incl the centroid.
        """
        for index, vtx in enumerate(self.v):
            self.v[index] = [self.M[0]*vtx[0]+self.M[1]*vtx[1]+self.M[2],\
                             self.M[3]*vtx[0]+self.M[4]*vtx[1]+self.M[5]]


# TODONT creer 3 transform : transforma, b, w normal, avec bounce avec wrap
# TODO : smart_pygdraw method, suivant flag retourné de border check

    # if self.x <= 0 or self.x + self.width >= window.width:

    #def bounce(self,dt):
    #        self.dx *= -1
    #    if self.y <= 0 or self.y + self.height >= window.height:
    #        self.dy *= -1


    #    self.x += self.dx * dt
    #    self.y += self.dy * dt
    #
    #    self.x = min(max(self.x, 0), window.width - self.width)
    #    self.y = min(max(self.y, 0), window.height - self.height)

##--- POINT -------------------------------------------------------------------
class Point(Grob):
    """ Point (x, y, color, transformation matrix)
    """
    def __init__(self,x, y, color, M=id_matrix()):
        self.v=[(x,y)]
        self.x = x
        self.y = y
        self._color = color # color
        self._M = M
        grobs.append(self)

    def __repr__(self):
        return "Point\t@(%.1d,%.1d), \t\t\t\tM%s" % ( self.x, self.y, self.M)

    def copy(self):
        new_point = Point (self.x0, self.y0, self.M)
        return new_point

    def pygdraw(self): #point is drawn as a 3 pixel rectangle on screen
        global pt
        e=pt*0.5 # extra pixels around point center
        pyglet.gl.glColor3f(self.color[0],self.color[1],self.color[2])
        glBegin(GL_QUADS)
        glVertex2f(self.x-e, self.y-e)    # bottom left
        glVertex2f(self.x+e, self.y-e)    # bottom right
        glVertex2f(self.x+e, self.y+e)    # top right
        glVertex2f(self.x-e, self.y+e)    # top left
        glEnd()

##--- SIMPLE LINE -------------------------------------------------------------
class SimpleLine(Grob):
    """ line, from (x0,y0) to (x1,y1).
    """
    def __init__(self,x0, y0, x1, y1, color=(0.3,0.3,0.3), M=id_matrix()):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self._color = color # color
        self._M = M
        grobs.append(self)

    def __repr__(self):
       return "Line \t(%.1d,%.1d), (%.1d,%.1d), M%s" \
       % (self.x0, self.y0, self.x1, self.y1, self.M)

    def copy(self):
        new_line= SimpleLine (self.x0, self.y0, self.x1, self.y1, self.M)
        return new_line
# TODO : point size fix
# TODO : point = rectangle
# TODO : repenser les representations, utiliser vtx ou VEC2D comme base ?

    def pygdraw(self, **kwargs):
        """ Draws a straight line to pyglet window
        with the current stroke color and strokewidth.
        """
        #fill, stroke, strokewidth, strokestyle = color_mixin(**kwargs)
        #if stroke is not None and strokewidth > 0:
        #    glColor4f(stroke[0], stroke[1], stroke[2], stroke[3] * _alpha)
        #    glLineWidth(strokewidth)
        #    glLineDash(strokestyle)
        pyglet.gl.glColor3f(self.color[0],self.color[1],self.color[2])
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.x0,self.y0)
        glVertex2f(self.x1,self.y1)
        glEnd()

        #pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (x0, y0, x1, y1)))


##--- SIMPLE RECTANGLE (ortho) ------------------------------------------------
class Rect(Grob):
    """ rectangle is defined by center x,y and size w,h
    """
    def __init__(self, width=300, height=100, xc=0, yc=0, \
                 color=(0,0,0), M=id_matrix()):
        # self vertex list:
        #                             centroid,     [0]
        #                             bottom left,  [1]
        #                             bottom right, [2]
        #                             top right,    [3]
        #                             top left      [4]
        self.v=[[xc,yc],[xc-width*0.5,yc-height*0.5],\
                        [xc+width*0.5,yc-height*0.5],\
                        [xc+width*0.5,yc+height*0.5],\
                        [xc-width*0.5,yc+height*0.5],]
        self.M = M
        self.color = color
        grobs.append(self)

    def __repr__(self):
       return "Rec\tw,h:(%.1dx%.1d), @(%.1d,%1d), \t\tM%3s" \
       % (self.width(), self.height(), self.v[0][0], self.v[0][1], self.M)

    def copy(self):
        rect=Rect(self.width(),self.height(),self.v[0][0],self.v[0][1],self.color,self.M)
        return rect

    def width(self):
        return(distance(self.v[1][0], self.v[1][1], self.v[2][0], self.v[2][1]))

    def height(self):
        return(distance(self.v[1][0], self.v[1][1], self.v[4][0], self.v[4][1]))

    def pygdraw(self, **kwargs):
        """ Draws the rectangle with the bottom left corner at x, y.
        The current stroke, strokewidth and fill color are applied.
        """
        pyglet.gl.glColor3f(self.color[0],self.color[1],self.color[2])
        glBegin(GL_QUADS)
        glVertex3f(self.v[1][0], self.v[1][1], 0.0)  # bottom left
        glVertex3f(self.v[2][0], self.v[2][1], 0.0)  # bottom right
        glVertex3f(self.v[3][0], self.v[3][1], 0.0)  # top right
        glVertex3f(self.v[4][0], self.v[4][1], 0.0)  # top left
        glEnd()

    def check_border(self,l,r,t,b):
        """ Draws the rectangle with the bottom left corner at x, y.
        The current stroke, strokewidth and fill color are applied.
        """
        pass
# --> following code from nodebox.context
#def rect(x, y, width, height, **kwargs):
#""" Draws a rectangle with the bottom left corner at x, y.
#    The current stroke, strokewidth and fill color are applied.
#"""
#fill, stroke, strokewidth, strokestyle = color_mixin(**kwargs)
#for i, clr in enumerate((fill, stroke)):
#    if clr is not None and (i==0 or strokewidth > 0):
#        if i == 1:
#            glLineWidth(strokewidth)
#            glLineDash(strokestyle)
#        glColor4f(clr[0], clr[1], clr[2], clr[3] * _alpha)
#        # Note: this performs equally well as when using precompile().


##--- GRID CELL ---------------------------------------------------------------

class Grid(Grob):
    """ grid centered on screen center
    """
    def __init__(self,cell_size, screen_size_x, screen_size_y, color =(0.23,0.23,0.23,1.0)):
        self.s = cell_size
        self.x0, self.y0 = -(screen_size_x*0.5) +1, -(screen_size_y*0.5) +1
        self.x1, self.y1 = (screen_size_x*0.5) +1, (screen_size_y*0.5) +1
        self.h = int( (screen_size_x*0.5)/self.s)
        self.v = int( (screen_size_y*0.5)/self.s)
        self._color = color # color
        grobs.append(self)

    def __repr__(self):
       return "Grid\t(%.1d)" % self.s

    def pygdraw(self):
        """ Draws a centered square grid, s = size of grid squares
        """
        pyglet.gl.glColor3f(self.color[0],self.color[1],self.color[2])

        for i in range(-self.v,self.v): # H lines
            d = i*self.s
            pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2f',\
            (self.x0,d,self.x1,d)))

        for i in range(-self.h,self.h): # V lines
            d = i*self.s
            pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2f',\
            (d,self.y1,d,self.y0)))

    def transform(self):
        print 'grid cannot be transformed !'


# TODO : creer eventuellement un grob gridcell
#class GridCell(Grob):

    #def __init__(self,width,height,cell_size=10):
    #
    #    self.cell_size = cell_size
    #    self.width = width
    #    self.height = height
    #    self.columns = self.width / self.cell_size
    #    self.rows = self.height / self.cell_size
    #    self._color = color # color
    #
    #def pixel_to_row(self,pixel_x, pixel_y):
    #    "Translate pixel coordinates (pixel_x,pixel_y), into grid coordinates"
    #    x = pixel_x * self.columns / self.screen_width + 1
    #    y = pixel_y * self.rows / self.screen_height  + 1
    #    return x,y
    #
    #def draw_cell(self, col, row):
    #    # Draw an OpenGL rectangle
    #    x1,y1 = (col-1) * self.cell_size, (row-1) * self.cell_size
    #    x2,y2 = (col-1) * self.cell_size + self.cell_size, (row-1) * \
    #    self.cell_size + self.cell_size
    #    pyglet.graphics.draw \
    #    (4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))
    #
    #def transform(self):
    #    """ applies own's transformation matrix to point.
    #    """
    #    pass

class Scope(Grob):
    """ Scope centered on screen center
    """
    def __init__(self,screen_size_x, screen_size_y, color =(0.5,0.03,0.03) ):
        self.x0, self.y0 = -(screen_size_x*0.5) +1, -(screen_size_y*0.5) +1
        self.x1, self.y1 = (screen_size_x*0.5) +1, (screen_size_y*0.5) +1
        self._color = color # color
        grobs.append(self)

    def __repr__(self):
       return "Scope "

    def pygdraw(self):
        """ Draws a centered scope
        """
        pyglet.gl.glColor3f(self.color[0],self.color[1],self.color[2])
        pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2f',(self.x0,0,self.x1,0)))
        pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2f',(0,self.y1,0,self.y0)))

    def transform(self):
        print 'scope cannot be transformed !'


##--- TRIANGLE ----------------------------------------------------------------
##--- POLYGON -----------------------------------------------------------------

# Polygon is a list of (x,y) pairs.
###
###def point_inside_polygon(x,y,poly):
###
###    n = len(poly)
###    inside =False
###
###    p1x,p1y = poly[0]
###
##--- ELLIPSE -----------------------------------------------------------------
##--- ELLIPSE -----------------------------------------------------------------
##--- BEZIER CURVE ------------------------------------------------------------
# --> see code @ nodebox.context.py


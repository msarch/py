#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# who : msarch@free.fr
# when : 04.2013
# what : elements géometriques 2d et fonctions graphiques associées
# 

# r0.3

##--- COMMENTS ----------------------------------------------------------------------------------------
# structure of this app stolen from : https://github.com/the-swerve/langtonsant
# parts inspired by nodeboxGL
# ...

##--- CONSTANTS ----------------------------------------------------------------------------------------

pt_size=2 # point size on screen

##--- IMPORTS ----------------------------------------------------------------------------------------

from pyglet.gl import *
from toxy import vmult

##--- CLASSES & FUNCTIONS ----------------------------------------------------------------------------------------


##--- ObGeom ----------------------------------------------------------------------------------------
# tous les objets geoms sont une liste de points, un basepoint, une couleur
# de cette facon ils peuvent partager certaines fonctions : draw, scale, rotate, move, mirror etc...
class ObGeom():
    pass

##--- SimplePoint-------------------------------------------------------------------------------------------
class Point(ObGeom):

    def __init__(self,x=0, y=0):
        self.x = x
        self.y = y
        self.lmnt_type = 'Point'
        self.pixel_size=2
        self.vertex_list=[[self.x,self.y]]
        
    def operate(self,m):
        """ applies to self the affine transformation defined by the matrix 'm'.
        """
        self.x,self.y=vmult(self.x,self.y,m)
      
    def __repr__(self):
        return "%s @(%.1d,%.1d)" % (self.__class__, self.x, self.y)
    
    def pygDraw(self):
        x1,y1 = int(self.x), int(self.y)                                    # bottom left
        x2,y2 = int(self.x+self.pixel_size), int(self.y)                    # bottom right
        x3,y3 = int(self.x+self.pixel_size), int(self.y+self.pixel_size)    # Top right 
        x4,y4 = int(self.x), int(self.y+self.pixel_size)                    # Top left
        
        glBegin(GL_QUADS)
        glVertex3f(x4, y4, 0.0)    # Top left
        glVertex3f(x3, y3, 0.0)    # Top right
        glVertex3f(x2, y2, 0.0)    # bottom right
        glVertex3f(x1, y1, 0.0)    # bottom left
        glEnd()
            
            
##--- SIMPLE LINE -------------------------------------------------------------------------------------------
     
class SimpleLine(ObGeom):
    
    def __init__(self, x0,y0,x1,y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.lmnt_type = 'SimpleLine'
    
    def operate(self,m):
        """ applies to self the affine transformation defined by the matrix 'm'.
        """
        self.x0,self.y0=vmult(self.x0,self.y0,m)
        self.x1,self.y1=vmult(self.x1,self.y1,m)

    def __repr__(self):
       return "%s : start@(%.1d,%.1d) end@(%.1d,%.1d)" % (self.__class__, self.x0, self.y0,self.x1,self.y1)

    def pygDraw(self, **kwargs):
        """ Draws a straight line to pyglet window
        with the current stroke color and strokewidth.
        """
        # --> following code from nodebox.context
        #fill, stroke, strokewidth, strokestyle = color_mixin(**kwargs)
        #if stroke is not None and strokewidth > 0:
        #    glColor4f(stroke[0], stroke[1], stroke[2], stroke[3] * _alpha)
        #    glLineWidth(strokewidth)
        #    glLineDash(strokestyle)
    
        x0,y0 = int(self.x0), int(self.y0)     # first point
        x1,y1 = int(self.x1), int(self.y1)     # second point
        
        # variante pour tracer une ligne
        #glBegin(GL_LINE_LOOP)
        #glVertex2f(x0, y0)
        #glVertex2f(x1, y1)
        #glEnd()

        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (x0, y0, x1, y1)))   


##--- SIMPLE RECTANGLE (ortho) -------------------------------------------------------------------------------------------

# faire aussi : rect rotated, operations différentes mais 
# tous les 2 se dessinent en GL comme un quad


class SimpleRec(ObGeom):
    """ Draws a rectangle with the bottom left corner at x, y.
    The current stroke, strokewidth and fill color are applied.
    """
    
    def __init__(self, x=0, y=0, width=10, height=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lmnt_type = 'SimpleRec'
        self.basepoint = [self.x,self.y,1]
        
    @property
    def centroid_x(self):
        return (self.x+0.5*self.width)
    
    @property
    def centroid_y(self):
        return (self.y+0.5*self.height) 

    def __repr__(self):
       return "%s @(%.1d,%.1d), size(w%.1dxh%.1d)" % (self.__class__, self.x, self.y, self.width, self.height)
    
    def operate(self,m):
        """ applies to self the affine transformation defined by the matrix 'm'.
        """
        self.x,self.y=vmult(self.x,self.y,m)

    def copy(self):
        new_rec= SimpleRec (self.x, self.y, self.width, self.height)
        return new_rec
    
    def pygDraw(self, **kwargs):
        """ Draws the rectangle with the bottom left corner at x, y.
        The current stroke, strokewidth and fill color are applied.
        """
        x1,y1 = int(self.x), int(self.y)                          # bottom left
        x2,y2 = int(self.x+self.width), int(self.y)               # bottom right
        x3,y3 = int(self.x+self.width), int(self.y+self.height)   # Top right 
        x4,y4 = int(self.x), int(self.y+self.height)              # Top left
        
        glBegin(GL_QUADS)
        glVertex3f(x4, y4, 0.0)    # Top left
        glVertex3f(x3, y3, 0.0)    # Top right
        glVertex3f(x2, y2, 0.0)    # bottom right
        glVertex3f(x1, y1, 0.0)    # bottom left
        glEnd()
              
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

#        
# 
    
##--- RECT rotated -------------------------------------------------------------------------------------------
##--- TRIANGLE -------------------------------------------------------------------------------------------
##--- POLYGON -------------------------------------------------------------------------------------------

# Polygon is a list of (x,y) pairs.
###
###def point_inside_polygon(x,y,poly):
###
###    n = len(poly)
###    inside =False
###
###    p1x,p1y = poly[0]
###    
##--- ELLIPSE -------------------------------------------------------------------------------------------
##--- ELLIPSE -------------------------------------------------------------------------------------------
##--- BEZIER CURVE -------------------------------------------------------------------------------------------           
# --> see code @ nodebox.context.py



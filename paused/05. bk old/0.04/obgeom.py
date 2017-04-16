#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# ms
# elements géometriques 2d et fonctions associées

# Rev 0.2

#--------------------------------------
#              comments
#--------------------------------------
# - Rev 0.1 :
#       - methodes de transformation
#       - listes d'elements <--> layers ?
#       - opération symetrie ( => liste de géométrie, axe)
#       - opération array ( => liste de géométrie, nx,ny,dx,dy)

#--------------------------------------
#              imports
#--------------------------------------



from pyglet.gl import *

#--------------------------------------
#         functions & classes
#--------------------------------------



#         SUPERCLASS : Geom
#--------------------------------------

# tous les objets geoms sont une liste de points, un basepoint, une couleur
# de cette facon ils peuvent patager les fonctions : draw, scale, rotate, move, mirror etc...
# for points in geom :
#   move point
#   return geom

class ObGeom():
    pass
##--- SIMPLE POINT -------------------------------------------------------------------------------------------
          
# --> from nodebox.geometry

class Point(ObGeom):
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.lmnt_type = 'Point'
        self.width=1
        self.height=1

    def _get_xy(self):
        return (self.x, self.y)
    
    def _set_xy(self, (x,y)):
        self.x = x
        self.y = y      
    
    def move(self, dx, dy):
        self.x = self.x+dx
        self.y = self.y+dy
      
    def __repr__(self):
        return "%s @ (%.1d, %.1d)" % (self.__class__, self.x, self.y)
    
    def pygDraw(self):
        """
        Based on the (r,g,b) color passed in, draw a point at the given x,y coord.
        """
        x1,y1 = int(self.x), int(self.y)                          # bottom left
        x2,y2 = int(self.x+self.width), int(self.y)               # bottom right
        x3,y3 = int(self.x+self.width), int(self.y+self.height)   # Top right 
        x4,y4 = int(self.x), int(self.y+self.height)              # Top left
        
        glBegin(GL_QUADS)
        glVertex3f(x4, y4, 0.0)	# Top left
        glVertex3f(x3, y3, 0.0)	# Top right
        glVertex3f(x2, y2, 0.0)	# bottom right
        glVertex3f(x1, y1, 0.0)	# bottom left
        glEnd()
            




##--- SIMPLE LINE -------------------------------------------------------------------------------------------
     
class SimpleLine(ObGeom):
    
    def __init__(self, point_0, point_1):
        self.point_0 = point_0
        self.point_1 = point_1
        self.lmnt_type = 'SimpleLine'
        
    def move(self, dx, dy):
        self.point_0.move(dx,dy)
        self.point_1.move(dx,dy)
        
    def __repr__(self):
       return "%s : from (%.1d, %.1d) to (%.1d, %.1d)" % (self.__class__, self.point_0.x, self.point_0.y,self.point_1.x,self.point_1.y)

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
    
        x0,y0 = int(self.point_0.x), int(self.point_0.y)     # first point
        x1,y1 = int(self.point_1.x), int(self.point_1.y)     # second point
        
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
    
    def __init__(self, pos_x=0, pos_y=0, width=1, height=1):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.lmnt_type = 'SimpleRec'
  
    def __repr__(self):
       return "%s @ (%.1d, %.1d),  width = %.1d,  height = %.1d" % (self.__class__, self.pos_x, self.pos_y, self.width, self.height)
    
    def move(self, dx, dy):
        self.pos_x = self.pos_x+dx
        self.pos_y = self.pos_y+dy
    

    #@property
    #posx,posy
    #
    #@property
    #tint
    #
    #def translate(self,vect2d ):
    #    pass
    #
    #@porperty
    #barycentre

    def pygDraw(self, **kwargs):
    
        x1,y1 = int(self.pos_x), int(self.pos_y)                          # bottom left
        x2,y2 = int(self.pos_x+self.width), int(self.pos_y)               # bottom right
        x3,y3 = int(self.pos_x+self.width), int(self.pos_y+self.height)   # Top right 
        x4,y4 = int(self.pos_x), int(self.pos_y+self.height)              # Top left
        
        glBegin(GL_QUADS)
        glVertex3f(x4, y4, 0.0)	# Top left
        glVertex3f(x3, y3, 0.0)	# Top right
        glVertex3f(x2, y2, 0.0)	# bottom right
        glVertex3f(x1, y1, 0.0)	# bottom left
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
#        glBegin((GL_POLYGON, GL_LINE_LOOP)[i])
#        glVertex2f(x, y)
#        glVertex2f(x+width, y)
#        glVertex2f(x+width, y+height)
#        glVertex2f(x, y+height)
#        glEnd()
#        
# 
    
##--- RECT rotated -------------------------------------------------------------------------------------------
##--- TRIANGLE -------------------------------------------------------------------------------------------
##--- ELLIPSE -------------------------------------------------------------------------------------------
##--- ELLIPSE -------------------------------------------------------------------------------------------
##--- BEZIER CURVE -------------------------------------------------------------------------------------------           
# --> see code @ nodebox.context.py



#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand/shapes :: rev 22 :: MAY2014 :: msarch@free.fr

from itertools import chain
from pyglet.graphics import vertex_list
from pyglet.gl import GL_TRIANGLE_STRIP
from pyglet.graphics import Batch

from debug import db_print

##--- CONSTANTS AND VARIABLES -------------------------------------------------

##---COLOR CLASS---------------------------------------------------------------
class Color(object):
    orange = (255, 127, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    red = (200, 0, 0)
    blue = (127, 127, 255)
    pink = (255, 187, 187)
    very_light_grey = (0.95, 0.95, 0.95, 0)
    kapla_colors = ((1.00, 0.84, 0.00),(0.00, 0.39, 0.00), (0.00, 0.39, 0.00),\
        (1.00, 0.27, 0.00), (0.00, 0.00, 0.55))


##---GENERAL GRAPHIC PRIMITIVE CLASS-------------------------------------------
class Primitive(object):
    """
    Stores a list of vertices, a single color, and a primitive type
    Intended to be rendered as a single OpenGL primitive
    """
    def __init__(self, verts, color, primtype=GL_TRIANGLE_STRIP):
        self.verts = verts
        self.color = color
        self.primtype = primtype
        self.vertex_list = None
        self.flat_verts = None

    def transform(self,M):
        """ applies matrix M transformation to all self vertexes
        """
        for index, v in enumerate(self.verts):
            self.verts[index] = [M[0]*v[0]+M[1]*v[1]+M[2],\
                                 M[3]*v[0]+M[4]*v[1]+M[5]]

    def offset(self, dx, dy):
        newverts = [(v[0] + dx, v[1] + dy) for v in self.verts]
        return Primitive(newverts, self.color, primtype=self.primtype)

    def rotate(self, alpha):
        print 'rotate not implemented'
        return(self)

    def get_flat_verts(self):
        if self.flat_verts is None:
            self.flat_verts = \
                list(self.verts[0]) + \
                [x for x in chain(*self.verts)] + \
                list(self.verts[-1])
        return self.flat_verts

    def get_vertexlist(self):
        if self.vertex_list is None:
            flatverts = self.get_flat_verts()
            numverts = len(flatverts) / 2
            self.vertex_list = vertex_list(
                numverts,
                ('v2f/static', flatverts),
                ('c3B/static', self.color * numverts))
        return self.vertex_list

# _________ TODO



    #@property
    #def type(self):
        #return (self.__class__)

    #@property
    #def M(self):
        #return (self._M)

    #@M.setter
    #def M(self,matrix):
        #self._M = matrix

    #@property
    #def color(self):
        #return (self._color)

    #@color.setter
    #def color(self,c):
        #self._color = c





    #def __repr__(self):
       #return "Rec\tw,h:(%.1dx%.1d), @(%.1d,%1d), \t\tM%3s" \
       #% (self.width(), self.height(), self.v[0][0], self.v[0][1], self.M)

    #def copy(self):
        #rect=Rect(self.width,self.height,self.v[0][0],self.v[0][1],self.color,self.M)
        #return rect


#---MULTI PRIMITIVES HOLDER----------------------------------------------------
class Shape(object):
    '''
    A list of primitives
    '''
    def __init__(self, items=None):
        self.primitives = []
        if items:
            self.add_items(items)
        self.batch = None

    def add_items(self, items):
        "Add a list of primitives and shapes"
        for item in items:
            if isinstance(item, Shape):
                self.add_shape(item)
            else:
                self.primitives.append(item)

    def add_shape(self, other):
        "Add the primitives from a given shape"
        for prim in other.primitives:
            self.primitives.append(prim)

    def get_batch(self):
        if self.batch is None:
            self.batch = Batch()
            for prim in self.primitives:
                flatverts = prim.get_flat_verts()
                numverts = len(flatverts) / 2
                self.batch.add(
                    numverts,
                    prim.primtype,
                    None,
                    ('v2f/static', flatverts),
                    ('c3B/static', prim.color * numverts)
                )
        return self.batch

    def transform(self,M):
        """ applies matrix M to all self primitives
        """
        for prim in self.primitives:
            prim.transform(M)



#---COMMON PRIMITIVES----------------------------------------------------------

class Rect(Primitive):
    """ (basepoint x,basepoint y), width, height,color
    v2                             v3
      +---------------------------+
      |                           |
      |                           |
      +---------------------------+
    vO                             v1

    glBegin(GL_TRIANGLE_STRIP);
    glVertex3fv(v0);
    glVertex3fv(v1);
    glVertex3fv(v2);
    glVertex3fv(v3);
    glEnd();
    """
    def __init__(self,x,y,w,h,color):
        verts=[(x,y),(x+w,y),(x,y+h),(x+w,y+h)]
        Primitive.__init__ (self,verts,color, GL_TRIANGLE_STRIP)

def Blip(x,y):
    print 'blip not implemented'
    pass

def Point(x,y):
    print 'point not implemented'
    pass


#class Rect2(Primitive):
    #""" rectangle is defined by center x,y and size w,h
    #"""
    #def __init__(self, width=300, height=100, xc=0, yc=0, \
                 #color=(0,0,0), M=id_matrix()):
        ## self vertex list:
        ##                             centroid,     [0]
        ##                             bottom left,  [1]
        ##                             bottom right, [2]
        ##                             top right,    [3]
        ##                             top left      [4]
        #self.v=[[xc,yc],[xc-width*0.5,yc-height*0.5],\
                        #[xc+width*0.5,yc-height*0.5],\
                        #[xc+width*0.5,yc+height*0.5],\
                        #[xc-width*0.5,yc+height*0.5],]



#def triangle(x1, y1, x2, y2, x3, y3, **kwargs):
#    """ Draws the triangle created by connecting the three given points.
#        The current stroke, strokewidth and fill color are applied.
#    """
#    fill, stroke, strokewidth, strokestyle = color_mixin(**kwargs)
#    for i, clr in enumerate((fill, stroke)):
#        if clr is not None and (i==0 or strokewidth > 0):
#            if i == 1:
#                glLineWidth(strokewidth)
#                glLineDash(strokestyle)
#            glColor4f(clr[0], clr[1], clr[2], clr[3] * _alpha)
#            # Note: this performs equally well as when using precompile().
#            glBegin((GL_POLYGON, GL_LINE_LOOP)[i])
#            glVertex2f(x1, y1)
#            glVertex2f(x2, y2)
#            glVertex2f(x3, y3)
#            glEnd()

#_ellipses = {}
#ELLIPSE_SEGMENTS = 50
#def ellipse(x, y, width, height, segments=ELLIPSE_SEGMENTS, **kwargs):
#    """ Draws an ellipse with the center located at x, y.
#        The current stroke, strokewidth and fill color are applied.
#    """
#    if not segments in _ellipses:
#        # For the given amount of line segments, calculate the ellipse once.
#        # Then reuse the cached ellipse by scaling it to the desired size.
#        _ellipses[segments] = []
#        for mode in (GL_POLYGON, GL_LINE_LOOP):
#            _ellipses[segments].append(precompile(lambda:(
#                glBegin(mode),
#               [glVertex2f(cos(t)/2, sin(t)/2) for t in [2*pi*i/segments for i in range(segments)]],
#                glEnd()
#            )))
#    fill, stroke, strokewidth, strokestyle = color_mixin(**kwargs)
#    for i, clr in enumerate((fill, stroke)):
#        if clr is not None and (i==0 or strokewidth > 0):
#            if i == 1:
#                glLineWidth(strokewidth)
#                glLineDash(strokestyle)
#            glColor4f(clr[0], clr[1], clr[2], clr[3] * _alpha)
#            glPushMatrix()
#            glTranslatef(x, y, 0)
#            glScalef(width, height, 1)
#            glCallList(_ellipses[segments][i])
#            glPopMatrix()

#oval = ellipse # Backwards compatibility.
##---TRANSFORMATION MATRIXES---------------------------------------------------

id_matrix = [1, 0, 0, 0, 1, 0, 0, 0, 1]  # Identity matrix
symX_matrix = [1, 0, 0, 0, -1, 0, 0, 0, 1]  # X axi symetry matrix
symY_matrix = [-1, 0, 0, 0, 1, 0, 0, 0, 1]  # Y axi symetry matrix

def trans_matrix(dx, dy):  # transformation matrix for a (dx,dy) translation
    return ([1, 0, dx, 0, 1, dy, 0, 0 ,1])

def rot_matrix(alpha):  # matrix for a rotation around 0,0
    print 'angle=', alpha, 'rot_matrix not implemented'
    pass

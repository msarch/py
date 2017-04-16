#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * july 2014 * bw-rev103
'''

#--- IMPORTS ------------------------------------------------------------------
from pyglet.gl import GL_TRIANGLE_STRIP, glPushMatrix, glTranslatef,\
    glRotatef, glPopMatrix
from . colors import Color
from . shapes import *

#--- COMMON PRIMITIVES --------------------------------------------------------
def Blip(x,y):
    print 'blip not implemented'
    pass


def Point(x,y):
    print 'point not implemented'
    pass


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
    def __init__(self,w,h,color):
        verts=[(0,0),(w,0),(0,h),(w,h)]
        Primitive.__init__ (self,verts,color, GL_TRIANGLE_STRIP)


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



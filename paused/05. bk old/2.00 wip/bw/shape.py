#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * jan 2015 * bw-rev113
portions from Jonathan Hartley's code
'''

#--- IMPORTS ------------------------------------------------------------------
from itertools import count, chain, ifilter

from pyglet.gl import glPushMatrix, glTranslatef,glRotatef, glPopMatrix
from pyglet.graphics import Batch

from bw.color import *  # all colors
from bw.dump import dumpObj
from bw.math import *

##--- GENERAL GRAPHIC SHAPE CLASS ---------------------------------------------
class Shape(object):
    '''
    Shape is a mixed list of:
    - other Shapes
    - base elements
        - list of vertices
        - RGBA color
        - single OpenGL prim: TRIANGLE_STRIP, LINE_STRIP, LINE , POINT
    '''
    shapes=[]
    
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])
        if not hasattr(self,'visible'):
            self.visible=True
        if not hasattr(self,'color'):
            self.color = red
        if not hasattr(self,'peg'):  # peg must be tuple (x, y, a)
            self.peg = DOCKED
        if not hasattr(self,'vel'):  # peg must be tuple (vx, vy, av)
            self.vel = IDLE
        if not hasattr (self,'pivot'):
            self.pivot=(0,0)  #  or pivot at AABB center ?? 
        if not hasattr (self,'shapes'):
            self.shapes=[]
        if not hasattr (self,'verts'):
            self.verts=[]  
        self.sort()
        self.flat_verts = None
        self.batch=None
        print ":: new shape", self.id
        Shape.shapes.append(self)

        dumpObj(self)

    def group(self,*args):
        '''
        Group items to  group list
        '''
        for sh in args:
            self.shapes.append(sh)  #add items
        print ":: GROUPED SHAPES"
        self.sort()

    def sort(self):
        if not self.shapes==[]:
            for s in self.shapes:
                print s.id,
            print
            self.shapes = sorted(self.shapes, key=lambda sh: sh.peg.z, reverse=True)
            print 'NEW ORDER',
            for s in self.shapes:
                print s.id,
            
    def get_flat_verts(self):
        if self.flat_verts is None:
            self.flat_verts = \
                list(self.verts[0]) + \
                [x for x in chain(*self.verts)] + \
                list(self.verts[-1])
        return self.flat_verts

    def get_batch(self):
        self.batch = Batch()
        flatverts = self.get_flat_verts()
        numverts = len(flatverts) / 2
        self.batch.add(
            numverts,
            self.primtype,
            None,
            ('v2f/static', flatverts),
            ('c4B/static', self.color * numverts)
            )

    def yeld_simple_shapes(self,root):
        if root.verts==[]:  #root is a set of shapes
            glPushMatrix()
            glTranslatef(root.peg.x, root.peg.y, 0)
            glRotatef(root.peg.angle, 0, 0, 1)
            for element in root.shapes:
                for e in self.yeld_simple_shapes(element):
                    yield e
            glPopMatrix()
        else:  #root is a shape itself
            yield root
            
    def yeld_verts(self):
        for sh in self.yeld_simple_shapes(self):
            for v in sh.verts:
                yield v
                
    def offset(self, dx, dy):
        '''
        offset will change the value of all the shapes vertexes
        '''
        newverts = [(v[0] + dx, v[1] + dy) for v in self.yeld_verts()]
        self.verts=newverts
        
    def gl_output(self):
        for sh in self.yeld_simple_shapes(self):
            if sh.batch is None:
                sh.get_batch()
            glPushMatrix()
            glTranslatef(sh.peg.x, sh.peg.y, 0)
            glRotatef(sh.peg.angle, 0, 0, 1)
            sh.batch.draw()
            print ('.'),
            glPopMatrix()

    @classmethod
    def draw(cls):
        visible_shapes = ifilter(lambda s: s.visible, cls.shapes)
        for sh in visible_shapes:
            cls.gl_output(sh)
        
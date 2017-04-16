#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * dec 2014 * bw-rev113
portions from Jonathan Hartley's code
'''

#--- IMPORTS ------------------------------------------------------------------
from itertools import chain
from pyglet.gl import glPushMatrix, glTranslatef,glRotatef, glPopMatrix
from pyglet.graphics import Batch
from utils.cfg import DOCKED,IDLE
from utils.cfg import *  # all colors
from utils.dump import dumpObj
from utils.math import *

##--- CONSTANTS AND VARIABLES -------------------------------------------------
##--- GENERAL GRAPHIC SHAPE CLASS ---------------------------------------------

_canvas=[]
class Shape(object):
    '''
    Shape is a mixed list of:
    - other Shapes
    - base elements
        - list of vertices
        - RGBA color
        - single OpenGL prim: TRIANGLE_STRIP, LINE_STRIP, LINE , POINT


    '''



    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])
        self.verts=[]
        self.shapes=[]
        self.build()
        if not hasattr(self,'color'):
            self.color = red
        if not hasattr(self,'peg'):  # peg must be tuple (x, y, a)
            self.peg = DOCKED
        if not hasattr(self,'vel'):  # peg must be tuple (vx, vy, av)
            self.vel = IDLE
        if not hasattr (self,'pivot'):
            self.pivot=(0,0)  #  or pivot at AABB center ??                   # TODO

        self.aabb=self.get_aabb()
        self.flat_verts = None
        self.batch=None
        print "::"
        print ":: new shape ::::::::::::::::::::::::::::::::::::::::::::::::::"
        print "::"
        dumpObj(self)

    def build(self):
        '''
        if this method isn't overridden the new element is either
            - a list of existing shapes
            - epmty
        '''
        pass


    def get_aabb(self): #                         POSSIBLE OPTIMIZATION       # TODO
        _allx=[0]
        _ally=[0]
        for v in self.verts:
            _allx.append(v[0])
            _ally.append(v[1])
        lox=min(_allx)
        loy=min(_ally)
        hix=max(_allx)
        hiy=max(_ally)
        return (AABB(lox,loy,hix,hiy))

    def copy(self):
        ssh=Shape(verts=self.verts, color=self.color,\
                primtype=self.primtype, peg=self.peg, vel=self.vel)
        return(ssh)

    def add(self,*args):
        '''
        Add items to the group list
        '''
        for sh in args:
            self.shapes.append(sh)  #add items
        self.sort()
        print "::"
        print ":: new actor ::::::::::::::::::::::::::::::::::::::::::::::::::"
        print "::"

    def sort(self):
        print ' REORDERING OF ACTORS NOT YET IMPLEMENTED'                         # TODO
        pass

    def get_instances(self,root):
        if root.shapes==[]:
            yield root
        else:
            glPushMatrix()
            glTranslatef(root.peg.x, root.peg.y, root.peg.z)
            glRotatef(root.peg.angle, 0, 0, 1)
            for element in root.shapes:
                for e in self.get_instances(element):
                    yield e
            glPopMatrix()

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

    def paint(self):
        for sh in self.get_instances(self):
            if sh.batch is None:
                sh.get_batch()
            glPushMatrix()
            glTranslatef(sh.peg.x, sh.peg.y, sh.peg.z)
            glRotatef(sh.peg.angle, 0, 0, 1)
            sh.batch.draw()
            glPopMatrix()
            print'.',


##--- MODULE FUNCTIONS --------------------------------------------------------
CANVAS=Shape()


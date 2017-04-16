#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * sept 2014 * bw-rev109
adapted from Jonathan Hartley's code
'''

#--- IMPORTS ------------------------------------------------------------------
from itertools import chain
import weakref

from pyglet.gl import GL_TRIANGLE_STRIP, GL_LINE_STRIP, \
        glPushMatrix, glTranslatef,glRotatef, glPopMatrix
from pyglet.graphics import Batch
from utils.cfg import DOCKED,IDLE
from utils.cfg import *  # all colors
from utils.dump import dumpObj
from utils.math import *

##--- CONSTANTS AND VARIABLES -------------------------------------------------
##--- GENERAL GRAPHIC SHAPE CLASS ---------------------------------------------

_shown=set()
_hidden=set()

class Shape(object):
    '''
    Shapes have Vertices, a single color, and a single OpenGL primitive
    '''
    _instances = set()

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])
        if not hasattr(self,'peg'):  # peg must be tuple (x, y, a)
            self.peg = DOCKED
        if not hasattr(self,'vel'):  # peg must be tuple (vx, vy, av)
            self.vel = IDLE
        self.build()
        self.aabb=get_aabb(self.verts)
        self.flat_verts = None
        self.batch=None
        self._instances.add(weakref.ref(self))
        print "::"
        print ":: new shape ::::::::::::::::::::::::::::::::::::::::::::::::::"
        print "::"
        dumpObj(self)

    @classmethod
    def get_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    def copy(self):
        ssh=Shape(verts=self.verts, color=self.color,\
                primtype=self.primtype, peg=self.peg, vel=self.vel)
        return(ssh)

    def get_flat_verts(self):
        if self.flat_verts is None:
            self.flat_verts = \
                list(self.verts[0]) + \
                [x for x in chain(*self.verts)] + \
                list(self.verts[-1])
        return self.flat_verts

    def get_batch(self):
        if self.batch is None:
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
        return self.batch

    def paint(self):
        batch = self.get_batch()
        glPushMatrix()
        glTranslatef(self.peg.x, self.peg.y, 0)
        glRotatef(self.peg.angle, 0, 0, 1)
        batch.draw()
        glPopMatrix()

    def build(self):
        pass

#--- MULTI SHAPES HOLDER ------------------------------------------------------
class Composite(object):
    '''
    a list of shapes _ Composites have shapes and a peg"
    '''
    _instances = set()

    def __init__(self, *args, **kwargs):
        self.shapes = []
        self.batch = None
        if args:
            self.add_items(args)
        for i in kwargs:
            setattr(self,i,kwargs[i])
        if not hasattr(self,'peg'):  # peg must be tuple (x, y, a)
            self.peg = DOCKED
        if not hasattr(self,'vel'):  # peg must be tuple (vx, vy, av)
            self.vel = IDLE
        self._instances.add(weakref.ref(self))

        print "::"
        print ":: new C shape ::::::::::::::::::::::::::::::::::::::::::::::::"
        print "::"
        dumpObj(self)

    @classmethod
    def get_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    def add_items(self, items):
        '''
        Add a list containing shapes and shapes
        '''
        for item in items:
            if isinstance(item, Composite):  #item is a C-shape
                for ssh in item.shapes:  #decompose item into shapes
                    ssh=ssh.copy() #mke a copy move it at new pos
                    ssh.verts = offset(ssh.verts, item.peg.x+ssh.peg.x, \
                            item.peg.y+ssh.peg.y)
                    self.shapes.append(ssh)  #add it
                    ssh.peg = DOCKED
                    ssh.vel = IDLE
            elif isinstance(item, Shape):
                ssh=item.copy()
                print ssh.verts,  ssh.peg.x, ssh.peg.y
                ssh.verts = offset(ssh.verts, ssh.peg.x, ssh.peg.y)
                print ssh.verts
                self.shapes.append(ssh)  # item is a shape, add a copy of it
                ssh.peg = DOCKED
                ssh.vel = IDLE

            else:
                pass

    def get_batch(self):
        print ':: getting C-Shape batch'
        print ':: self batch is :', self.batch
        if self.batch is None:
            self.batch = Batch()
            print ':: new batch :'
            for ssh in self.shapes:
                print ':: shape :', ssh
                flatverts = ssh.get_flat_verts()
                numverts = len(flatverts) / 2
                self.batch.add(
                    numverts,
                    ssh.primtype,
                    None,
                    ('v2f/static', flatverts),
                    ('c4B/static', ssh.color * numverts)
                )
        return self.batch

    def paint(self):
        print ':: displaying C-Shape :', self
        batch = self.get_batch()
        glPushMatrix()
        glTranslatef(self.peg.x, self.peg.y, 0)
        glRotatef(self.peg.angle, 0, 0, 1)
        batch.draw()
        # OPTIMISATION : cs.batch.draw() directement avec batch déjà à jour TODO
        glPopMatrix()
        print ''


def paint_all():
    '''
    module level function : paints all shapes and c-shapes instances
    '''
    print ':: displaying all Composite shapes :',
    for csh in Composite.get_instances():
            csh.paint()
    print ':: +'

    print ':: displaying all unique shapes :'
    for ssh in Shape.get_instances():
            ssh.paint()
    print ':: +'

def show(*args):
    _shown.update(args)
    print _shown

def paint():
    for sh in _shown:
        sh.paint()
        print'.',

#--- COMMON SHAPES ------------------------------------------------------------
class Blip(Shape):
    """
    Point, autocad style
    color=color
    """
    def build(self):
        if not hasattr(self,'color'):
            self.color = red
        self.verts = [(-5,0),(5,0),(0,0),(0,5),(0,-5)]
        self.primtype = GL_LINE_STRIP

class Rose(Shape):
    '''
    Oriented Blip : north is marked
    '''
    def build(self):
        if not hasattr(self,'color'):
            self.color = red
        self.verts = [(-5,0),(5,0),(1,0),(1,5),(-1,5),(-1,0),(0,0),(0,-5)]
        self.primtype = GL_LINE_STRIP


class Rect(Shape):
    """
    Rectangle, lower left basepoint is @ origin
    w=width, h=height, color=color
    """

    def build(self):
        if not hasattr(self,'color'):
            self.color = white
        if not hasattr(self,'w'):
            self.w = 100
        if not hasattr(self,'h'):
            self.h = 50

        self.verts = [(0, 0),(self.w, 0),(0, self.h),(self.w, self.h)]
        self.primtype = GL_TRIANGLE_STRIP

        # 2--------3
        # |        |
        # 0--------1


class Kapla(Shape):
    """
    color=color
    """
    def build(self):
        if not hasattr(self,'color'):
            self.color = black
        self.w, self.h = 33,11
        self.verts = [(0,0),(self.w,0),(0,self.h),(self.w,self.h)]
        self.primtype = GL_TRIANGLE_STRIP






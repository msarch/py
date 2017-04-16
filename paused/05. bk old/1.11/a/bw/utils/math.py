#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Parts : Copyright (c) 2010 by Casey Duncan and contributors

import math
from cfg import AABB

def cached_property(func):
    '''
    Special property decorator that caches the computed
    property value in the object's instance dict the first
    time it is accessed.
    '''

    def getter(self, name=func.func_name):
        try:
            return self.__dict__[name]
        except KeyError:
            self.__dict__[name] = value = func(self)
            return value

    getter.func_name = func.func_name
    return property(getter, doc=func.func_doc)

def cos_sin_deg(deg):
    '''
    Return the cosine and sin for the given angle
    in degrees, with special-case handling of multiples
    of 90 for perfect right angles
    (by Casey Duncan and contributors)
    '''
    deg = deg % 360.0
    if deg == 90.0:
        return 0.0, 1.0
    elif deg == 180.0:
        return -1.0, 0
    elif deg == 270.0:
        return 0, -1.0
    rad = math.radians(deg)
    return math.cos(rad), math.sin(rad)
'''
A trois coordonnées, avec des matrices qui sont toujours carrées,
on peut composer plusieur transformations en multipliant les matrices
correspondant à chaque opération DANS UN ORDRE PRECIS.
Si le point 2D devient artificielement un vecteur à 3 coordonnées (x,y,z)
(par défaut on fixe z=1), la matrice générale des transformations 2d devient :
		[x']   [a b m]   [x]   [ax + by + mz]   [ax + by + mz]
		[y'] = [c d n] * [y] = [cx + dy + nz] = [cx + dy + nz]
		[z']   [0 0 1]   [z]   [0x + 0y + 1z]	   [     1      ]
Nous quittons maintenant le domaine de la géométrie euclidienne pour entrer
dans celui de la géométrie projective, outil géométrique très puissant.

Matrice type de mise à l'échelle
--------------------------------
		[Sx  0  0]
		[ 0 Sy  0]
		[ 0  0  1]
Matrice de rotation
------------------
		[ cosθ −sinθ    0]
		[ sinθ  cosθ    0]
                [   0     0     1]
'''

def offset_matrix(dx, dy):
    '''
    Transformation matrix for a (dx,dy) translation
                    [ 1  0  dx]
                    [ 0  1  dy]
                    [ 0  0   1]
    '''
    return ([1, 0, dx, 0, 1, dy, 0, 0 ,1])

def transform(verts, M):
    '''
    applies matrix M transformation to all self vertexes
    '''
    newverts = [ (M[0]*v[0]+M[1]*v[1]+M[2],
            M[3]*v[0]+M[4]*v[1]+M[5]) for v in verts]
    return(newverts)

def offset(verts,dx,dy):
    newverts = [(v[0] + dx, v[1] + dy) for v in verts]
    return(newverts)

def center_of_gravity(verts):
    x=345
    y=123  # calculate center or specific to shape?
    return(x,y)


def get_aabb(verts):
    _allx=[]
    _ally=[]
    for v in verts:
        _allx.append(v[0])
        _ally.append(v[1])
    lox=min(_allx)
    loy=min(_ally)
    hix=max(_allx)
    hiy=max(_ally)
    return (AABB(lox,loy,hix,hiy))



#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * july 2014 * bw-rev103
'''

##---TRANSFORMATION MATRIXES---------------------------------------------------
id_matrix = [1, 0, 0, 0, 1, 0, 0, 0, 1]  # Identity matrix
symX_matrix = [1, 0, 0, 0, -1, 0, 0, 0, 1]  # X axi symetry matrix
symY_matrix = [-1, 0, 0, 0, 1, 0, 0, 0, 1]  # Y axi symetry matrix

def trans_matrix(dx, dy):  # transformation matrix for a (dx,dy) translation
    return ([1, 0, dx, 0, 1, dy, 0, 0 ,1])

def rot_matrix(alpha):  # matrix for a rotation around 0,0
    print 'angle=', alpha, 'rot_matrix not implemented'
    pass

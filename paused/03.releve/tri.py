#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

"""

       A +---------+ B   alpha +--L-+ beta
         |         |            \   |
         |         |             N  M
         |         |              \ |
         |         |               \|
       D +---------+ C        gamma +

"""
	# {{{ function fold ...
    # }}}

#--------------------------------------
#                  *
#              imports
#                  *
#--------------------------------------
# {{{ (imports)
import sys
from math import *
import os
#FIXME redefinition of unused 'os' from line 12

try:
    import dxfwrite
except ImportError:
# if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    import os
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))
import dxfwrite
from dxfwrite import DXFEngine as dxf
#}}}
#--------------------------------------
#                  *
#             constants
#                  *
#--------------------------------------
#{{{ --> constants
z=0
#}}}
#--------------------------------------
#                  *
#             interface
#                  *
#--------------------------------------
# {{{ (interfaces functions)
def splash_screen():
    print'           A +---------+ B'
    print'             |         |'
    print'             |         |'
    print'             |         |'
    print'             |         |'
    print'           D +---------+ C'



def num_user_input(prompt):
    """
    > valide l'input
    > boucle si non valide
    > annulation possible : TODO
    > Args : prompt (string)
    > Returns : user_input (float)
    """
    user_input= 0
	while True:
		try:
			user_input = float(raw_input(prompt))
		except ValueError:
			print("--> non pris en compte")
			print("--> entrez 0 pour une mesure inexistante")
			continue
		else:
			return (num_input)

def print_results():
    pass


    # {{{
    # print resolution (A1,B1,C1)
    # print resolution (A2,B2,C2)
    pass
    # }}}
#
def dxf_out()
    # {{{
# TODO
#liste de points
#    ouverture fichier dxf
#        sortie des lignes dxf
#    fermeture fichier dxf
#    fin

def build_dwg(list_of_elements,dwgname)
    dwg = dxf.drawing(dwgname)
    def li(a,b):
    	dwg.add(dxf.line((0, 0), (C1 , 0), color=1, linetype='SOLID'))
    for polygons in list_of_elements.....
        drawing.add_layer('LINES')
        drawing.add(dxf.line((0, 0), (1, 0), color=7, layer='LINES')
        dwg.add(dxf.line((0, 0), (C1 , 0), color=1, linetype='SOLID'))
        dwg.add(dxf.line((C1, 0), (C1, -A1), color=2, linetype='SOLID'))

    dwg.save()
    print("drawing '%s' created.\n" % dwgname)
    # }}}
# }}}
#--------------------------------------
#                  *
#        functions & classes
#                  *
#--------------------------------------
# {{{  -->  internal functions & classes

def cos_sin_deg(deg):
    # stolen from  Casey Duncan' planar module
    """Return the cosine and sin for the given angle
    in degrees, with special-case handling of multiples
    of 90 for perfect right angles
    """
    deg = deg % 360.0
    if deg == 90.0:
        return 0.0, 1.0
    elif deg == 180.0:
        return -1.0, 0
    elif deg == 270.0:
        return 0, -1.0
    rad = math.radians(deg)
    return math.cos(rad), math.sin(rad)

class Triangle
    """
    > definit triangle
    > calculs
    > annulation possible : TODO
    > Args : prompt (string)
    > Returns : user_input (float)
    """

    def al_kashi (l,m,n):
        """ doc string ...
        > Calcule les 3 angles : alpha, beta, gamma
        d'un triangle a partir des trois longueurs : L,M,N
                    alpha +--L-+ beta
                           \   |
                            N  M
                             \ |
                              \|
                         gamma +
        > Args : L,M,N (float,float,float)
        > Returns : alpha,beta,gamma (float,float,float)
        """
        alpha = degrees(acos(( b**2 + c**2 -a**2)/(2*b*c)))
        beta = degrees(acos(( a**2 + c**2 -b**2)/(2*a*c)))
        gamma = degrees(acos(( a**2 + b**2 -c**2)/(2*a*b)))
        return (alpha,beta,gamma)


# }}}
#--------------------------------------
#                  *
#                main
#                  *
#--------------------------------------
# {{{ * main *
# TODO

splash_screen()
input
calc
print results

for polygons in list :
    dxfout(polygon)
print ok
exit

# }}}
#--------------------------------------

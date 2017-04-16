#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Author:  msarch@free.fr
# Purpose: draws a square room from a list of measurements
# Created:   .  .2012
# License: MIT License

    """ {{{ module docstring...
    > valide l'input
    > boucle si non valide
    > annulation possible
    > Args :    a (string)i
                x (float)
    > Returns : myoutput (float)
    > Raises:   TypeError: if n is not a number.
                ValueError: if n is negative.
    """ #}}}
#--------------------------------------
#              imports
#--------------------------------------
# {{{ (imports)
import sys
# if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
try:
    import dxfwrite
except ImportError:
    import os
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))
import dxfwrite
from dxfwrite import DXFEngine as dxf
#}}}
#--------------------------------------
#             constants
#--------------------------------------
#{{{ (constants)
#
#
#
#}}}
#--------------------------------------
#          exception classes
#--------------------------------------
# {{{ (exceptions classes)
# ?
#}}}
#--------------------------------------
#   internal functions & classes
#--------------------------------------
# {{{ (functions and classes)

#          Class : MyClass
#-----------------------------------------------
class MyClass(object):
    """ {{{ docstring...
    > MyClass docstring...
    """ # }}}
    # {{{ class fold ...
    def my_method(self):
        """The method's docstring"""
    # }}}

#         function : functionA
#-----------------------------------------------
def functionA(arg1,arg2):
    """ {{{ docstring...
    > valide l'input
    > boucle si non valide
    > annulation possible
    > Args :    a (string)i
                x (float)
    > Returns : myoutput (float)
    > Raises:   TypeError: if n is not a number.
                ValueError: if n is negative.
    """ # }}}
    #{{{ function fold ...
    pass
    #}}}


# 	   function : validate user input
#-----------------------------------------------
def num_user_input(prompt)
    """ {{{ docstring...
    > valide l'input
    > boucle si non valide
    > annulation possible : NOT IMPLEMENTED
    > Args : prompt (string)
    > Returns : num_imput (float)
    """ #}}}
    #{{{ function ...
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
    #}}}

#               functionB
#--------------------------------------------------
def functionB(a,b):
    #{{{ function
    #
    #}}}

#
dwg.save()
print("drawing '%s' created.\n" % dwgname)
exit()

# }}}
#--------------------------------------
#                main
#--------------------------------------
# {{{ (main)
def main(...):
    ...

if __name__ == '__main__':
    status = main()
    sys.exit(status)
# }}}

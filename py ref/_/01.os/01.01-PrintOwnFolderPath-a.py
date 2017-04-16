#! /usr/bin/python
# -*- coding: latin-1 -*-      # permet les accents dans le script
import sys, os
script= sys.argv[0]  # le premier element de argv est le nom du script, les suivants: parametres
chemin= os.path.abspath(script)  # chemin + nom du script
repertoire= os.path.dirname(chemin)  # retourne la partie chemin
print repertoire

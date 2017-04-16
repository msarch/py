#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 13-e :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from squirtle import getsvg
from engine import Engine

##  CONSTANTS AND VARIABLES ---------------------------------------------------
obj=[]
ruleset=[]
##  --- FUNCTIONS -------------------------------------------------------------
obj.append (getsvg('kapla.svg'))




##  MAIN ----------------------------------------------------------------------
def main():
    options={ 'DEBUG' : 1,
            'END_TIME' : 3, # EXPORT MODE : duration (seconds) of the anim
            'PREVIEW_SIZE' : (800,600),
            'BGCOLOR' : (0.95, 0.95, 0.95, 0),# background
            'FPS' : 60, # display max framerate
            'PicPS' : 25,  # EXPORT MODE FRAMERATE : images per second for movie export
            'MODE' : 'PREVIEW', # options are : 'FULL'; 'PREVIEW'; 'EXPORT'
            'OBJ' : obj
            }
    engine=Engine(**options)
    engine.run()

##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()



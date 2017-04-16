#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: main :: rev 16 :: 01.2014 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------
from scene import Scene
from engine import Engine

##  CONSTANTS AND VARIABLES ---------------------------------------------------

##  --- FUNCTIONS -------------------------------------------------------------

##  MAIN ----------------------------------------------------------------------
def main():
    options={ 'DEBUG' : 1,
            'PREVIEW_SIZE' : (800,600),
            'BGCOLOR' : (0.95, 0.95, 0.95, 0),# background
            'FPS' : 60, # display max framerate
            'PicPS' : 25,  # EXPORT MODE FRAMERATE : images per second for movie export
            'MODE' : 'PREVIEW', # options are : 'FULL'; 'PREVIEW'; 'EXPORT'
            }
    engine=Engine(**options)
    scene1=Scene(folder='scene1', duration=3)
    scene1.configure()
    engine.run(scene1)

##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()




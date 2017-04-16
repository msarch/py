#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# msarch@free.fr * jan 2015 * bw-rev113


#--- Imports ------------------------------------------------------------------
from pyglet.window import get_platform

#--- DISPLAY INFO -------------------------------------------------------------
_screen = get_platform().get_default_display().get_default_screen()
WIDTH, HEIGHT = _screen.width*1.0 ,_screen.height*1.0
ASPECT = WIDTH / HEIGHT
CENTX, CENTY = WIDTH*0.5, HEIGHT*0.5
SCREEN = (-CENTX, -CENTY, CENTX, CENTY)




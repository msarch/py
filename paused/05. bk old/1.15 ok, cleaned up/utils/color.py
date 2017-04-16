#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# msarch@free.fr * dec 2014 * bw-rev113
# portions from Tom De Smedt, Frederik De Bleser NodeBox API


_background  = None    # Current state background color.
_fill        = None    # Current state fill color.
_stroke      = None    # Current state stroke color.
_strokewidth = 1       # Current state strokewidth.
_strokestyle = "solid" # Current state strokestyle.
_alpha       = 1       # Current state alpha transparency.

#--- COLOR CLASS --------------------------------------------------------------




#--- COLORS -------------------------------------------------------------------
orange  =(255, 127,   0, 255)
white   =(255, 255, 255, 255)
black   =(  0,   0,   0, 255)
yellow  =(255, 255,   0, 255)
red     =(255,   0,   0, 255)
blue    =(127, 127, 255, 255)
blue50  =(127, 127, 255, 127)
pink    =(255, 187, 187, 255)
very_light_grey =(242, 242, 242, 255)

# kapla_colors
r_k =(255, 69,   0,   255)  # red kapla
b_k =(  0,  0, 140,   255)  # blue kapla
g_k =(  0, 99,   0,   255)  # green kapla
y_k =(255, 214,  0,   255)  # yellow kapla
kapla_colors=(r_k, g_k, b_k, y_k, b_k)  # addded 1 color for pb  w 4 kaplas     TODO

def set_background_color(color=white):
    glClearColor(*blue)

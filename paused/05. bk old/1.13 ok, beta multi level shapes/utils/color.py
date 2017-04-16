#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
'''
msarch@free.fr * dec 2014 * bw-rev113
portions from Tom De Smedt, Frederik De Bleser NodeBox API

'''

import pyglet

from pyglet.gl    import *
from pyglet.image import Texture
from math         import cos, sin, radians, pi, floor
from time         import time
from random       import seed, choice, shuffle, random as rnd
from new          import instancemethod
from glob         import glob
from os           import path, remove
from sys          import getrefcount
from StringIO     import StringIO
from hashlib      import md5
from types        import FunctionType
from datetime     import datetime


#=====================================================================================================
#--- COLOR CLASS --------------------------------------------------------------

RGB = "RGB"
HSB = "HSB"
XYZ = "XYZ"
LAB = "LAB"

_background  = None    # Current state background color.
_fill        = None    # Current state fill color.
_stroke      = None    # Current state stroke color.
_strokewidth = 1       # Current state strokewidth.
_strokestyle = "solid" # Current state strokestyle.
_alpha       = 1       # Current state alpha transparency.

class Color(list):

    def __init__(self, *args, **kwargs):
        """ A color with R,G,B,A channels, with channel values ranging between 0.0-1.0.
            Either takes four parameters (R,G,B,A), three parameters (R,G,B),
            two parameters (grayscale and alpha) or one parameter (grayscale or Color object).
            An optional base=1.0 parameter defines the range of the given parameters.
            An optional colorspace=RGB defines the color space of the given parameters.
        """
        # Values are supplied as a tuple.
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        # R, G, B and A.
        if len(args) == 4:
            r, g, b, a = args[0], args[1], args[2], args[3]
        # R, G and B.
        elif len(args) == 3:
            r, g, b, a = args[0], args[1], args[2], 1
        # One value, grayscale and alpha.
        elif len(args) == 1:
            r, g, b, a = args[0], args[0], args[0], 1


    def _get_r(self): return self[0]
    def _get_g(self): return self[1]
    def _get_b(self): return self[2]
    def _get_a(self): return self[3]

    def _set_r(self, v): self[0] = v
    def _set_g(self, v): self[1] = v
    def _set_b(self, v): self[2] = v
    def _set_a(self, v): self[3] = v

    r = red   = property(_get_r, _set_r)
    g = green = property(_get_g, _set_g)
    b = blue  = property(_get_b, _set_b)
    a = alpha = property(_get_a, _set_a)

    def _get_rgb(self):
        return self[0], self[1], self[2]

    def _set_rgb(self, (r,g,b)):
        self[0] = r
        self[1] = g
        self[2] = b

    rgb = property(_get_rgb, _set_rgb)

    def _get_rgba(self):
        return self[0], self[1], self[2], self[3]
    def _set_rgba(self, (r,g,b,a)):
        self[0] = r
        self[1] = g
        self[2] = b
        self[3] = a

    rgba = property(_get_rgba, _set_rgba)

    def copy(self):
        return Color(self)

    def _apply(self):
        glColor4f(self[0], self[1], self[2], self[3] * _alpha)

    def __repr__(self):
        return "Color(%.3f, %.3f, %.3f, %.3f)" % \
            (self[0], self[1], self[2], self[3])

    def __eq__(self, clr):
        if not isinstance(clr, Color): return False
        return self[0] == clr[0] \
           and self[1] == clr[1] \
           and self[2] == clr[2] \
           and self[3] == clr[3]

    def __ne__(self, clr):
        return not self.__eq__(clr)

    def map(self, base=1.0, colorspace=RGB):
        """ Returns a list of R,G,B,A values mapped to the given base,
            e.g. from 0-255 instead of 0.0-1.0 which is useful for setting image pixels.
            Other values than RGBA can be obtained by setting the colorspace (RGB/HSB/XYZ/LAB).
        """
        r, g, b, a = self
        if colorspace != RGB:
            if colorspace == HSB: r, g, b = rgb_to_hsb(r, g, b)
            if colorspace == XYZ: r, g, b = rgb_to_xyz(r, g, b)
            if colorspace == LAB: r, g, b = rgb_to_lab(r, g, b)
        if base != 1:
            r, g, b, a = [ch*base for ch in r, g, b, a]
        if base != 1 and isinstance(base, int):
            r, g, b, a = [int(ch) for ch in r, g, b, a]
        return r, g, b, a

    def blend(self, clr, t=0.5, colorspace=RGB):
        """ Returns a new color between the two colors.
            Parameter t is the amount to interpolate between the two colors
            (0.0 equals the first color, 0.5 is half-way in between, etc.)
            Blending in CIE-LAB colorspace avoids "muddy" colors in the middle of the blend.
        """
        ch = zip(self.map(1, colorspace)[:3], clr.map(1, colorspace)[:3])
        r, g, b = [geometry.lerp(a, b, t) for a, b in ch]
        a = geometry.lerp(self.a, len(clr)==4 and clr[3] or 1, t)
        return Color(r, g, b, a, colorspace=colorspace)

    def rotate(self, angle):
        """ Returns a new color with it's hue rotated on the RYB color wheel.
        """
        h, s, b = rgb_to_hsb(*self[:3])
        h, s, b = rotate_ryb(h, s, b, angle)
        return Color(h, s, b, self.a, colorspace=HSB)

color = Color

def background(*args, **kwargs):
    """ Sets the current background color.
    """
    global _background
    if args:
        _background = Color(*args, **kwargs)
        xywh = (GLint*4)(); glGetIntegerv(GL_VIEWPORT, xywh); x,y,w,h = xywh
        rect(x, y, w, h, fill=_background, stroke=None)
    return _background

def fill(*args, **kwargs):
    """ Sets the current fill color for drawing primitives and paths.
    """
    global _fill
    if args:
        _fill = Color(*args, **kwargs)
    return _fill

fill(0) # The default fill is black.

def stroke(*args, **kwargs):
    """ Sets the current stroke color.
    """
    global _stroke
    if args:
        _stroke = Color(*args, **kwargs)
    return _stroke

def nofill():
    """ No current fill color.
    """
    global _fill
    _fill = None

def nostroke():
    """ No current stroke color.
    """
    global _stroke
    _stroke = None

def strokewidth(width=None):
    """ Sets the outline stroke width.
    """
    # Note: strokewidth is clamped to integers (e.g. 0.2 => 1),
    # but finer lines can be achieved visually with a transparent stroke.
    # Thicker strokewidth results in ugly (i.e. no) line caps.
    global _strokewidth
    if width is not None:
        _strokewidth = width
        glLineWidth(width)
    return _strokewidth

SOLID  = "solid"
DOTTED = "dotted"
DASHED = "dashed"

def strokestyle(style=None):
    """ Sets the outline stroke style (SOLID / DOTTED / DASHED).
    """
    global _strokestyle
    if style is not None and style != _strokestyle:
        _strokestyle = style
        glLineDash(style)
    return _strokestyle

def glLineDash(style):
    if style == SOLID:
        glDisable(GL_LINE_STIPPLE)
    elif style == DOTTED:
        glEnable(GL_LINE_STIPPLE); glLineStipple(0, 0x0101)
    elif style == DASHED:
        glEnable(GL_LINE_STIPPLE); glLineStipple(1, 0x000F)

def outputmode(mode=None):
    raise NotImplementedError

def colormode(mode=None, range=1.0):
    raise NotImplementedError

#--- COLOR SPACE -------------------------------------------------------------------------------------
# Transformations between RGB, HSB, CIE XYZ and CIE LAB color spaces.
# http://www.easyrgb.com/math.php

def rgb_to_hsb(r, g, b):
    """ Converts the given R,G,B values to H,S,B (between 0.0-1.0).
    """
    h, s, v = 0, 0, max(r, g, b)
    d = v - min(r, g, b)
    if v != 0:
        s = d / float(v)
    if s != 0:
        if   r == v: h = 0 + (g-b) / d
        elif g == v: h = 2 + (b-r) / d
        else       : h = 4 + (r-g) / d
    h = h / 6.0 % 1
    return h, s, v

def hsb_to_rgb(h, s, v):
    """ Converts the given H,S,B color values to R,G,B (between 0.0-1.0).
    """
    if s == 0:
        return v, v, v
    h = h % 1 * 6.0
    i = floor(h)
    f = h - i
    x = v * (1-s)
    y = v * (1-s * f)
    z = v * (1-s * (1-f))
    if i > 4:
        return v, x, y
    return [(v,z,x), (y,v,x), (x,v,z), (x,y,v), (z,x,v)][int(i)]

def rgb_to_xyz(r, g, b):
    """ Converts the given R,G,B values to CIE X,Y,Z (between 0.0-1.0).
    """
    r, g, b = [ch > 0.04045 and ((ch+0.055) / 1.055) ** 2.4 or ch / 12.92 for ch in r, g, b]
    r, g, b = [ch * 100.0 for ch in r, g, b]
    r, g, b = ( # Observer = 2, Illuminant = D65
        r * 0.4124 + g * 0.3576 + b * 0.1805,
        r * 0.2126 + g * 0.7152 + b * 0.0722,
        r * 0.0193 + g * 0.1192 + b * 0.9505)
    return r/95.047, g/100.0, b/108.883

def xyz_to_rgb(x, y, z):
    """ Converts the given CIE X,Y,Z color values to R,G,B (between 0.0-1.0).
    """
    x, y, z = x*95.047, y*100.0, z*108.883
    x, y, z = [ch / 100.0 for ch in x, y, z]
    r = x *  3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y *  1.8758 + z *  0.0415
    b = x * -0.0557 + y * -0.2040 + z *  1.0570
    r, g, b = [ch > 0.0031308 and 1.055 * ch**(1/2.4) - 0.055 or ch * 12.92 for ch in r, g, b]
    return r, g, b

def rgb_to_lab(r, g, b):
    """ Converts the given R,G,B values to CIE L,A,B (between 0.0-1.0).
    """
    x, y, z = rgb_to_xyz(r, g, b)
    x, y, z = [ch > 0.008856 and ch**(1/3.0) or (ch*7.787) + (16/116.0) for ch in x, y, z]
    l, a, b = y*116-16, 500*(x-y), 200*(y-z)
    l, a, b = l/100.0, (a+86)/(86+98), (b+108)/(108+94)
    return l, a, b

def lab_to_rgb(l, a, b):
    """ Converts the given CIE L,A,B color values to R,G,B (between 0.0-1.0).
    """
    l, a, b = l*100, a*(86+98)-86, b*(108+94)-108
    y = (l+16)/116.0
    x = y + a/500.0
    z = y - b/200.0
    x, y, z = [ch**3 > 0.008856 and ch**3 or (ch-16/116.0)/7.787 for ch in x, y, z]
    return xyz_to_rgb(x, y, z)

def luminance(r, g, b):
    """ Returns an indication (0.0-1.0) of how bright the color appears.
    """
    return (r*0.2125 + g*0.7154 + b+0.0721) * 0.5

def darker(clr, step=0.2):
    """ Returns a copy of the color with a darker brightness.
    """
    h, s, b = rgb_to_hsb(clr.r, clr.g, clr.b)
    r, g, b = hsb_to_rgb(h, s, max(0, b-step))
    return Color(r, g, b, len(clr)==4 and clr[3] or 1)

def lighter(clr, step=0.2):
    """ Returns a copy of the color with a lighter brightness.
    """
    h, s, b = rgb_to_hsb(clr.r, clr.g, clr.b)
    r, g, b = hsb_to_rgb(h, s, min(1, b+step))
    return Color(r, g, b, len(clr)==4 and clr[3] or 1)

darken, lighten = darker, lighter

#--- COLOR ROTATION ----------------------------------------------------------------------------------

# Approximation of the RYB color wheel.
# In HSB, colors hues range from 0 to 360,
# but on the color wheel these values are not evenly distributed.
# The second tuple value contains the actual value on the wheel (angle).
_colorwheel = [
    (  0,   0), ( 15,   8), ( 30,  17), ( 45,  26),
    ( 60,  34), ( 75,  41), ( 90,  48), (105,  54),
    (120,  60), (135,  81), (150, 103), (165, 123),
    (180, 138), (195, 155), (210, 171), (225, 187),
    (240, 204), (255, 219), (270, 234), (285, 251),
    (300, 267), (315, 282), (330, 298), (345, 329), (360, 360)
]

def rotate_ryb(h, s, b, angle=180):
    """ Rotates the given H,S,B color (0.0-1.0) on the RYB color wheel.
        The RYB colorwheel is not mathematically precise,
        but focuses on aesthetically pleasing complementary colors.
    """
    h = h*360 % 360
    # Find the location (angle) of the hue on the RYB color wheel.
    for i in range(len(_colorwheel)-1):
        (x0, y0), (x1, y1) = _colorwheel[i], _colorwheel[i+1]
        if y0 <= h <= y1:
            a = geometry.lerp(x0, x1, t=(h-y0)/(y1-y0))
            break
    # Rotate the angle and retrieve the hue.
    a = (a+angle) % 360
    for i in range(len(_colorwheel)-1):
        (x0, y0), (x1, y1) = _colorwheel[i], _colorwheel[i+1]
        if x0 <= a <= x1:
            h = geometry.lerp(y0, y1, t=(a-x0)/(x1-x0))
            break
    return h/360.0, s, b

def complement(clr):
    """ Returns the color opposite on the color wheel.
        The complementary color contrasts with the given color.
    """
    if not isinstance(clr, Color):
        clr = Color(clr)
    return clr.rotate(180)

def analog(clr, angle=20, d=0.1):
    """ Returns a random adjacent color on the color wheel.
        Analogous color schemes can often be found in nature.
    """
    h, s, b = rgb_to_hsb(*clr[:3])
    h, s, b = rotate_ryb(h, s, b, angle=random(-angle,angle))
    s *= 1 - random(-d,d)
    b *= 1 - random(-d,d)
    return Color(h, s, b, len(clr)==4 and clr[3] or 1, colorspace=HSB)

#--- COLOR MIXIN -------------------------------------------------------------------------------------
# Drawing commands like rect() have optional parameters fill and stroke to set the color directly.

def color_mixin(**kwargs):
    fill        = kwargs.get("fill", _fill)
    stroke      = kwargs.get("stroke", _stroke)
    strokewidth = kwargs.get("strokewidth", _strokewidth)
    strokestyle = kwargs.get("strokestyle", _strokestyle)
    return (fill, stroke, strokewidth, strokestyle)
#--- COLORS -------------------------------------------------------------------
orange  = Color(255, 127,   0, 255)
white   = Color(255, 255, 255, 255)
black   = Color(  0,   0,   0, 255)
yellow  = Color(255, 255,   0, 255)
red     = Color(255,   0,   0, 255)
blue    = Color(127, 127, 255, 255)
blue50  = Color(127, 127, 255, 127)
pink    = Color(255, 187, 187, 255)
very_light_grey = Color(242, 242, 242, 0)

# kapla_colors
r_k = Color(255, 69,   0,   255)  # red kapla
b_k = Color(  0,  0, 140,   255)  # blue kapla
g_k = Color(  0, 99,   0,   255)  # green kapla
y_k = Color(255, 214,  0,   255)  # yellow kapla
kapla_colors=(r_k, g_k, b_k, y_k, b_k)  # addded 1 color for pb  w 4 kaplas     TODO

def set_background_color(color=white):
    glClearColor(*blue)

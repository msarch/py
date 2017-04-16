#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from PIL import Image
import aggdraw

img = Image.new("RGB", (2000, 2000), "white")

# Draw(image_or_mode, size, color=None)
# Creates a drawing interface object.
# - image_or_mode
#   A PIL Image, or a mode string. The following modes are supported: ÒLÓ, ÒRGBÓ, ÒRGBAÓ, ÒBGRÓ, ÒBGRAÓ.
# - size
#   If a mode string was given, this argument gives the image size, as a 2-tuple.
# - color
#   An optional background color specifier. If a mode string was given, this is used to initialize the image memory. If omitted, it defaults to white with full alpha.

canvas = aggdraw.Draw(img)

# Draw(image_or_mode, size, color=None) (class) [#]
# Creates a drawing interface object. The constructor can either take a PIL Image object, or mode and size specifiers.
#
# Examples:
#
#   d = aggdraw.Draw(im)
#
#   d = aggdraw.Draw("RGB", (800, 600), "white")
#image_or_mode
#A PIL Image, or a mode string. The following modes are supported: ÒLÓ, ÒRGBÓ, ÒRGBAÓ, ÒBGRÓ, ÒBGRAÓ.
#size
#If a mode string was given, this argument gives the image size, as a 2-tuple.
#color
#An optional background color specifier. If a mode string was given, this is used to initialize the image memory. If omitted, it defaults to white with full alpha.

brush = aggdraw.Brush("Red",200)

# Creates a brush object.
# - color
#   Brush color. This can be a color tuple, a CSS-style color name, or a color integer (0xaarrggbb).
# - opacity=
#   Optional brush opacity. The default is to create a solid brush.
pen = aggdraw.Pen("black",5,200)
#
# Pen(color, width=1, opacity=255) [#]
# Creates a pen object.
#
# - color
# Pen color. This can be a color tuple, a CSS-style color name, or a color integer (0xaarrggbb).
# - width=
# Optional pen width.
# - opacity=
# Optional pen opacity. The default is to create a solid pen.


p = aggdraw.Path()
p.moveto(0,0)
p.rlineto(300, 300)
p.curveto(500, -200)
p.rlineto(10,300)
p.close()
canvas.path((100,1000), p, pen,brush)
canvas.path((10,900), p, pen,brush)

canvas.flush()


img.save("curve.png", "PNG")
img.show()
#################################################################
links : matrix or table use  (type 'gx' to open url)
http://stackoverflow.com/questions/15312273/traverse-a-graph-represented-in-an-adjacency-matrix?rq=1
http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch20s05.html
#################################################################

#!/usr/bin/env python
"""\
Usage: drawsvg.py file
file  - one SVG file (from Inkscape!) that is all simple paths

"""
##    svg2py Copyright  (C)  2007 Donn.C.Ingle
##    http://cairographics.org/svgtopycairo/
##    Contact: donn.ingle@gmail.com - I hope this email lasts.
##
SVG paths can be parsed and turned into a seqence of cairo commands that re-draw them.

This took a while, the pyparsing had me in knots, but now it's short and sweet.
A fuller implementation of what can be done in SVG would be really nice. (Hint...)

Make sure you pass it a very simple SVG file (from Inkscape is best)
-- one that has had all the shapes reduced to paths.
Oh, and keep your canvas 400 by 400 or it may draw clear off the screen.

Depends on

elementree: import elementree as myDearWatson :) It's a great module for slicing through XML.
pyparsing: This module is deeply wonderful. I won't pretend to savvy even 1% of it, but it really does the job. They have a great mailing list where I got a lot of help. It let's you parse strings into lists and that is no small feat.
SVG Path element

To briefly explain, inside an svg file (which is just xml) you'll find a tag named 'g' and under that one or more tags named 'path'. Inside path there is an element called 'd'; that's the actual path. It's formed like this: "COMMAND NUMBER COMMA NUMBER Optionally[NUMBER COMMA NUMBER a few more times]", where COMMAND is M for move, L for line, C for curve and Z for close path. There may be others, but that's what I tackled. Have a look at the pyparsing grammar which makes it fairly clear how different commands have different numbers behind them.##

import pygtk
pygtk.require('2.0')
import gtk, gobject, cairo
from pyparsing import *
import os, sys
from elementtree import ElementTree as et

# Create a GTK+ widget on which we will draw using Cairo
class Screen(gtk.DrawingArea):

    # Draw in response to an expose-event
    __gsignals__ = { "expose-event": "override" }

    # Handle the expose-event by drawing
    def do_expose_event(self, event):

        # Create the cairo context
        cr = self.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()

        self.draw(cr, *self.window.get_size())

    def draw(self, cr, width, height):
        # Fill the background with gray
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.rectangle(0, 0, width, height)
        cr.fill()

# GTK mumbo-jumbo to show the widget in a window and quit when it's closed
def run(Widget):
    window = gtk.Window()
    window.set_size_request(400, 400)
    window.connect("delete-event", gtk.main_quit)
    widget = Widget()
    widget.show()
    window.add(widget)
    window.present()
    gtk.main()

## Do the drawing ##

class Shapes(Screen):
    def draw(self, ctx, width, height):

        #Build a string of cairo commands
        cairo_commands = ""
        command_list = []
        for tokens in paths:
            for command,couples in tokens[:-1]: #looks weird, but it works :)
                c = couples.asList()
                if command == "M":
                    cairo_commands += "ctx.move_to(%s,%s);" % (c[0],c[1])
                if command == "C":
                    cairo_commands += "ctx.curve_to(%s,%s,%s,%s,%s,%s);" % (c[0],c[1],c[2],c[3],c[4],c[5])
                if command == "L":
                    cairo_commands += "ctx.line_to(%s,%s);" % (c[0],c[1])
                if command == "Z":
                    cairo_commands += "ctx.close_path();"

            command_list.append(cairo_commands) #Add them to the list
            cairo_commands = ""
        #Draw it. Only stroked, to fill as per the SVG drawing is another whole story.
        ctx.set_source_rgb(1,0,0)
        for c in command_list:
            exec(c)
        ctx.stroke()

#################################################################

#Check args:
if len(sys.argv) < 2:
    raise SystemExit(__doc__)
file = sys.argv[1]

#################################################################

## Pyparsing grammar:
## With HUGE help from Paul McGuire <paul@alanweberassociates.com>
## Thanks!
dot = Literal(".")
comma = Literal(",").suppress()
floater = Combine(Optional("-") + Word(nums) + dot + Word(nums))
## Unremark to have numbers be floats rather than strings.
#floater.setParseAction(lambda toks:float(toks[0]))
couple = floater + comma + floater
M_command = "M" + Group(couple)
C_command = "C" + Group(couple + couple + couple)
L_command = "L" + Group(couple)
Z_command = "Z"
svgcommand = M_command | C_command | L_command | Z_command
phrase = OneOrMore(Group(svgcommand))

## Find and open the svg file
xml_file = os.path.abspath(__file__)
xml_file = os.path.dirname(xml_file)
xml_file = os.path.join(xml_file, file)

tree = et.parse(xml_file)

ns = "http://www.w3.org/2000/svg" #The XML namespace.
paths = []
for group in tree.getiterator('{%s}g' % ns):
    for e in group.getiterator('{%s}path' % ns):
        p = e.get("d")
        tokens = phrase.parseString(p.upper())
        paths.append(tokens) # paths is a global var.

run(Shapes)


#################################################################

def cos_sin_deg(deg):
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


#################################################################




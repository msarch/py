##	Things Copyright(C) 2009 Donn.C.Ingle
##
##	Contact: donn.ingle@gmail.com - I hope this email lasts.
##
##  This file is part of Things.
##
##  Things is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  Things is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with Things.  If not, see <http://www.gnu.org/licenses/>.

# SVG to pyCairo : 30 March 2009
# This class takes SVG (xml) and produces python-cairo code
# that will draw the same thing.

# This is needed for things like paths and clips and hit-masks where
# the data is needed in Cairo -- pyRSVG can't send that data to Cairo
# (As far as I can tell. And, boy, have I looked...)

import pyparsing as PP
from xml.dom import minidom 
from bugs import Bugs as _Bugs

## Describe the syntax of Inkscape SVG path and style strings
_dot = PP.Literal(".")
_comma = PP.Literal(",").suppress()

# floater is a floating point number
#floater = PP.Combine(PP.Optional("-") + PP.Word(PP.nums) + _dot + PP.Word(PP.nums)) 

## This has E- in the string... C -12.247076,-45.821257 -5.6365193,-44.150318 8.8683224E-07,-45.345722
## Hence I had to add gumf into _floater.
_floater = PP.Combine(PP.Optional("-") + PP.Word(PP.nums) + _dot + PP.Word(PP.nums) + PP.Optional( PP.Literal("E") + PP.Literal("-") + PP.Word(PP.nums) ) ) 
_floater.setParseAction(lambda toks:float(toks[0]))

_couple = _floater + _comma + _floater
_M_command = "M" + PP.Group(_couple)
_C_command = "C" + PP.Group(_couple + _couple + _couple)
_L_command = "L" + PP.Group(_couple)
_Z_command = "Z"
_svgCommand = _M_command | _C_command | _L_command | _Z_command
_svgPhrase = PP.OneOrMore(PP.Group(_svgCommand)) 

##Style grammar - once again, saved by Paul
_floatOrInt = PP.Combine(PP.Word(PP.nums) + PP.Optional(PP.Literal(".") + PP.Word(PP.nums)))
_px = PP.Suppress("px")
_hexNums = PP.Suppress("#") + PP.Word(PP.hexnums) | PP.Word("none")
_semi = PP.Literal(";").suppress()
_COLON = PP.Literal(":").suppress()
_FILL_command = "fill" + _COLON + _hexNums + PP.Optional(_semi)
_FILLOPACITY_command = "fill-opacity" + _COLON + _floatOrInt + PP.Optional(_semi)
_STROKECOLOR_command = "stroke" + _COLON + _hexNums + PP.Optional(_semi)
_STROKEWIDTH_command = "stroke-width" + _COLON + _floatOrInt + PP.Optional(_px) + PP.Optional(_semi)
_STROKEOPACITY_command = "stroke-opacity" + _COLON + _floatOrInt + PP.Optional(_semi)
svgStylePhrase = _FILL_command | _FILLOPACITY_command | _STROKECOLOR_command | _STROKEWIDTH_command | _STROKEOPACITY_command


# Moved this into a module: 1 april 2009.
def parsePathElement( pathNode ): 
	d = pathNode.getAttribute('d')
	s = pathNode.getAttribute('style')
	cpc = doD(d)
	csc = doStyle(s)
	commands = {'paths':cpc, 'styles':csc}

	return commands

# The pyparsing magic stuff:
def doD( path ):
	path = path.upper()
	try:
		tokens = _svgPhrase.parseString( path )
		## Build a string of cairo commands, keep it as tight as possible.
		cpc = ""					 
		for group in tokens:
			command = group[0]
			if command == "Z":
				cpc += "ctx.close_path();"
			else:
				c = group[1]
				if command == "M":
					cpc += "ctx.move_to(%s,%s);" %(c[0], c[1])
				if command == "C":
					cpc += "ctx.curve_to(%s,%s,%s,%s,%s,%s);" %(c[0], c[1], c[2], c[3], c[4], c[5]) 
				if command == "L":
					cpc += "ctx.line_to(%s,%s);" %(c[0], c[1])
	except:
		raise _Bugs("BAD_SVG_PATH", id=id)
	return cpc 

def doStyle( style ):
	try:
		csc = ""
		tokens = svgStylePhrase.searchString( style )
		d = dict(tokens.asList())
		## The styles are different, we are picking only a few for now.
		try:
			rgb = d["fill"]
		except:
			rgb = "000000"
		try:
			a = d["fill-opacity"]
		except:
			a = 1
		csc += "ctx.set_source_rgba(%s);" % _hexToFloat( rgb, a )
		csc += "ctx.fill_preserve();"
		try:
			rgb = d["stroke"]
		except:
			rgb = "000000"
		try:
			px = d["stroke-width"]
		except:
			px = 1
		try:
			a = d["stroke-opacity"]
		except:
			a = 1
		csc += "ctx.set_source_rgba(%s);" % _hexToFloat( rgb, a )
		csc += "ctx.set_line_width(%s);" % px
		csc += "ctx.stroke();"
	except:
		print "BAD:",csc
		raise
		raise _Bugs( "BAD_SVG_STYLE", id=id )
		
	return csc

def _hexToFloat( h, a ):
	"""Private: convert rrggbb hex and alpha to a four string return, each from 0 to 1."""
	if h == "none": return "0,0,0,0"
	r, g, b = h[:2], h[2:4], h[4:]
	r, g, b = [(int(n, 16)/256.0) for n in (r, g, b)]
	return "%s,%s,%s,%s" % (r,g,b,a)
	return commands







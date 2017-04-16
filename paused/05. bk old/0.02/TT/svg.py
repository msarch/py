# Based on Nodebox-svg library,
# SVG parser
# TT mod : begin porting from Nodebox to NodeboxGL

import arc
import xml.dom.minidom as parser
import re           #regular expressions lib
from nodebox.graphics import context as _ctx

#### SVG PARSER ######################################################################################

def parse(svg, cached=False, _copy=True):

    dom = parser.parseString(svg)
    paths = parse_node(dom, [])

    return paths

def get_attribute(element, attribute, default=0):

    """ Returns XML element's attribute, or default if none.
    """

    a = element.getAttribute(attribute)
    if a == "":
        return default
    return a

#--- XML NODE ----------------------------------------------------------------------------------------

def parse_node(node, paths=[], ignore=["pattern"]):

    """ Recurse the node tree and find drawable tags.

    Recures all the children in the node.
    If a child is something we can draw,
    a line, rect, oval or path,
    parse it to a PathElement drawable with drawpath()

    """

    # Ignore paths in Illustrator pattern swatches etc.
    if node.nodeType == node.ELEMENT_NODE and node.tagName in ignore:
        return []

    if node.hasChildNodes():
        for child in node.childNodes:
            paths = parse_node(child, paths)

    if node.nodeType == node.ELEMENT_NODE:

        if node.tagName == "line":
            paths.append(parse_line(node))
        elif node.tagName == "rect":
            paths.append(parse_rect(node))
        elif node.tagName == "circle":
            paths.append(parse_circle(node))
        elif node.tagName == "ellipse":
            paths.append(parse_oval(node))
        elif node.tagName == "polygon":
            paths.append(parse_polygon(node))
        elif node.tagName == "polyline":
            paths.append(parse_polygon(node))
        elif node.tagName == "path":
            paths.append(parse_path(node))


    return paths

#--- LINE --------------------------------------------------------------------------------------------

def parse_line(e):

    x1 = float(get_attribute(e, "x1"))
    y1 = float(get_attribute(e, "y1"))
    x2 = float(get_attribute(e, "x2"))
    y2 = float(get_attribute(e, "y2"))
    p = _ctx.line(x1, y1, x2, y2, draw=False)
    return p

#--- RECT --------------------------------------------------------------------------------------------

def parse_rect(e):

    x = float(get_attribute(e, "x"))
    y = float(get_attribute(e, "y"))
    w = float(get_attribute(e, "width"))
    h = float(get_attribute(e, "height"))
    p = _ctx.rect(x, y, w, h, draw=False)
    return p

#--- CIRCLE -----------------------------------------------------------------------------------------

def parse_circle(e):

    x = float(get_attribute(e, "cx"))
    y = float(get_attribute(e, "cy"))
    r = float(get_attribute(e, "r"))
    p = _ctx.oval(x-r, y-r, r*2, r*2, draw=False)
    return p

#--- OVAL -------------------------------------------------------------------------------------------

def parse_oval(e):

    x = float(get_attribute(e, "cx"))
    y = float(get_attribute(e, "cy"))
    w = float(get_attribute(e, "rx"))*2
    h = float(get_attribute(e, "ry"))*2
    p = _ctx.oval(x-w/2, y-h/2, w, h, draw=False)
    return p

#--- POLYGON -----------------------------------------------------------------------------------------

def parse_polygon(e):

    d = get_attribute(e, "points", default="")
    d = d.replace(" ", ",")
    d = d.replace("-", ",")
    d = d.split(",")
    points = []
    for x in d:
        if x != "": points.append(float(x))

    _ctx.autoclosepath()
    if (e.tagName == "polyline") :
        _ctx.autoclosepath(False)

    _ctx.beginpath(points[0], points[1])
    for i in range(len(points)/2):
        _ctx.lineto(points[i*2], points[i*2+1])
    p = _ctx.endpath(draw=False)
    return p

#--- PATH --------------------------------------------------------------------------------------------

def parse_path(e):

    d = get_attribute(e, "d", default="")

    # Divide the path data string into segments.
    # Each segment starts with a path command,
    # usually followed by coordinates.
    segments = []
    i = 0
    for j in range(len(d)):
        commands = ["M", "m", "Z", "z", "L", "l", "H", "h", "V", "v", "C","c", "S", "s", "A"]
        if d[j] in commands:
            segments.append(d[i:j].strip())
            i = j
    segments.append(d[i:].strip())
    segments.remove("")

    previous_command = ""

    # Path origin (moved by MOVETO).
    x0 = 0
    y0 = 0

    # The current point in the path.
    dx = 0
    dy = 0

    # The previous second control handle.
    dhx = 0
    dhy = 0

    _ctx.autoclosepath(False)
    _ctx.beginpath(0,0)
    for segment in segments:

        command = segment[0]

        if command in ["Z", "z"]:
            _ctx.closepath()
        else:
            # The command is a pen move, line or curve.
            # Get the coordinates.
            points = segment[1:].strip()
            points = points.replace("-", ",-")
            points = points.replace(" ", ",")
            points = re.sub(",+", ",", points)
            points = points.strip(",")
            points = [float(i) for i in points.split(",")]

        # Absolute MOVETO.
        # Move the current point to the new coordinates.
        if command == "M":
            for i in range(len(points)/2):
                _ctx.moveto(points[i*2], points[i*2+1])
                dx = points[i*2]
                dy = points[i*2+1]
                x0 = dx
                y0 = dy

        # Relative MOVETO.
        # Offset from the current point.
        elif command == "m":
            for i in range(len(points)/2):
                _ctx.moveto(dx+points[i*2], dy+points[i*2+1])
                dx += points[i*2]
                dy += points[i*2+1]
                x0 = dx
                y0 = dy

        # Absolute LINETO.
        # Draw a line from the current point to the new coordinate.
        elif command == "L":
            for i in range(len(points)/2):
                _ctx.lineto(points[i*2], points[i*2+1])
                dx = points[i*2]
                dy = points[i*2+1]

        # Relative LINETO.
        # Offset from the current point.
        elif command == "l":
            for i in range(len(points)/2):
                _ctx.lineto(dx+points[i*2], dy+points[i*2+1])
                dx += points[i*2]
                dy += points[i*2+1]

        # Absolute horizontal LINETO.
        # Only the vertical coordinate is supplied.
        elif command == "H":
            for i in range(len(points)):
                _ctx.lineto(points[i], dy)
                dx = points[i]

        # Relative horizontal LINETO.
        # Offset from the current point.
        elif command == "h":
            for i in range(len(points)):
                _ctx.lineto(dx+points[i], dy)
                dx += points[i]

        # Absolute vertical LINETO.
        # Only the horizontal coordinate is supplied.
        if command == "V":
            for i in range(len(points)):
                _ctx.lineto(dx, points[i])
                dy = points[i]

        # Relative vertical LINETO.
        # Offset from the current point.
        elif command == "v":
            for i in range(len(points)):
                _ctx.lineto(dx, dy+points[i])
                dy += points[i]

        # Absolute CURVETO.
        # Draw a bezier with given control handles and destination.
        elif command == "C":
            for i in range(len(points)/6):
                _ctx.curveto(points[i*6],   points[i*6+1],
                             points[i*6+2], points[i*6+3],
                             points[i*6+4], points[i*6+5])
                dhx = points[i*6+2]
                dhy = points[i*6+3]
                dx = points[i*6+4]
                dy = points[i*6+5]

        # Relative CURVETO.
        # Offset from the current point.
        elif command == "c":
            for i in range(len(points)/6):
                _ctx.curveto(dx+points[i*6],   dy+points[i*6+1],
                             dx+points[i*6+2], dy+points[i*6+3],
                             dx+points[i*6+4], dy+points[i*6+5])
                dhx = dx+points[i*6+2]
                dhy = dy+points[i*6+3]
                dx += points[i*6+4]
                dy += points[i*6+5]

        # Absolute reflexive CURVETO.
        # Only the second control handle is given,
        # the first is the reflexion of the previous handle.
        elif command == "S":
            for i in range(len(points)/4):
                if previous_command not in ["C", "c", "S", "s"]:
                    dhx = dx
                    dhy = dy
                else:
                    dhx = dx-dhx
                    dhy = dy-dhy
                _ctx.curveto(dx+dhx, dy+dhy,
                             points[i*4],   points[i*4+1],
                             points[i*4+2], points[i*4+3])
                dhx = points[i*4]
                dhy = points[i*4+1]
                dx = points[i*4+2]
                dy = points[i*4+3]

        # Relative reflexive CURVETO.
        # Offset from the current point.
        elif command == "s":
            for i in range(len(points)/4):
                if previous_command not in ["C", "c", "S", "s"]:
                    dhx = dx
                    dhy = dy
                else:
                    dhx = dx-dhx
                    dhy = dy-dhy
                _ctx.curveto(dx+dhx, dy+dhy,
                             dx+points[i*4],   dy+points[i*4+1],
                             dx+points[i*4+2], dy+points[i*4+3])
                dhx = dx+points[i*4]
                dhy = dy+points[i*4+1]
                dx += points[i*4+2]
                dy += points[i*4+3]

        # Absolute elliptical arc.
        elif command == "A":
            rx, ry, phi, large_arc_flag, sweep_flag, x2, y2 = points
            for p in arc.elliptical_arc_to(dx, dy, rx, ry, phi, large_arc_flag, sweep_flag, x2, y2):
                if len(p) == 2:
                    _ctx.lineto(*p)
                elif len(p) == 6:
                    _ctx.curveto(*p)
            dx = p[-2]
            dy = p[-1]

        previous_command = command

    p = _ctx.endpath(draw=False)
    return p



# Add the upper directory (where the nodebox module is) to the search path.
import os, sys; sys.path.insert(0, os.path.join(".."))
import amethyst
from nodebox.graphics import *
#----------------------------------------------------
# COLORS
#----------------------------------------------------

mycolor1=(0.1, 1.0, 0.1, 1.0) # r,g,b,alpha
mycolor2=color(amethyst.triplet("red"))  # my color dictionnary lib

stroke(0.0, 0.25) # 75% transparent black.
strokewidth(1)

    # Clear the current stroke,
    # otherwise it is still active in the next frame
    # when we start drawing the rectangle and the ellipse.
    # nostroke()

    # You can also pass Color objects to fill() and stroke().
    # A Color object can be created with the color command.
    # It has clr.r, clr.g, clr.b, clr.a properties :
    #   clr = color(0.25, 0.15, 0.75, 0.5) # 50% transparent purple/blue.
    #   fill(clr)

    # If necessary, you can break away from the state and colorize and transform elements individually.
    # Each of the primitive commands
    # (line(), rect(), oval(), star(), arrow()), beginpath(), drawpath() and text()
    # have three optional parameters: fill, stroke and strokewidth.

def draw(canvas):
    canvas.clear()
    nofill()
    background(mycolor2)
	# background(0.1, 0.0, 0.1, 0.25)                      --> is ok
	# background(color(amethyst.color("red")))	            --> is ok too
    rect(50, 50, 50, 50)
    triangle(200, 200, 250, 300, 300, 200)
# While rect() and ellipse() expect x, y, width, height parameters,
# triangle() expects the coordinates of three points,
# which are connected into a triangle.
    rect(110, 50, 50, 50, stroke=Color(0), strokestyle=DASHED)
    stroke(mycolor1)
    strokewidth(5)
    rect(170, 50, 50, 50)
canvas.size = 500, 500
canvas.run(draw)


# Add the upper directory (where the nodebox module is) to the search path.
import os, sys; sys.path.insert(0, os.path.join("..",".."))

from nodebox.graphics import *

# Often, you may need groups of shapes that you can transform as a whole.
# For example: a planet that has moons rotating around it.
# The planet+moons is a group that as a whole rotates around a sun.

txt = Text("moon")

def draw(canvas):

    canvas.clear()

    stroke(0, 0.2)

    # Put the origin point in the center of the canvas.
    translate(canvas.width/2, canvas.height/2)
    line(0,0,0,30)
    push()
    rotate(canvas.frame) # Rotate around sun.
    line(0, 0, 120, 0)               # Draw a (rotated) line with length 120.
    # Increase rotation.
    pop()
    #rotate(canvas.frame *6)
                     # Move the origin back to the sun. Undo rotation.

canvas.size = 500, 500
canvas.run(draw)

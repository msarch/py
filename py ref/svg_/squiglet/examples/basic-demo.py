import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from pyglet import app, clock, graphics, gl
from pyglet.window import Window, mouse
from pyglet.window.key import symbol_string

from squiglet import Vector

win = Window()

class Ship(object):
    def __init__(self,colour):
        self.vector = Vector(colour,"ship.sgl")
        self.pos = (0,0)
    def draw(self):
        self.vector.draw(7,self.pos)

ships = [Ship((255,0,0)),Ship((0,255,0)),Ship((0,0,255))]

@win.event
def on_draw():
    win.clear()
    for ship in ships:
        ship.draw()

@win.event
def on_mouse_motion(x,y,dx,dy):
    offset = -60
    for ship in ships:
        ship.pos = (x+offset,y)
        offset+=60



app.run()

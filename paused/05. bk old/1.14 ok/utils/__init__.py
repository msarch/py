
#--- Imports ------------------------------------------------------------------
from pyglet.window import get_platform
from color import *
from collections import namedtuple

#--- VARS ---------------------------------------------------------------------
#--- CONSTANTS ----------------------------------------------------------------

Peg = namedtuple('Peg','x y z angle')
Vel = namedtuple('Vel','vx vy av')
Vel2 = namedtuple('Speed1', 'speed heading')
Vel3 = namedtuple('Speed2', 'x y angle speed')
Vel4 = namedtuple('Peg2', 'speed head_to') # or use Peg3 ??
Vel5 = namedtuple('Peg3', 'speed path') # target

Point  = namedtuple('Point', 'x y')
AABB = namedtuple('AABB', 'lox loy hix hiy')

ORIGIN = Point(0.0, 0.0)
IDLE   = Vel(0.0, 0.0, 0.0)
DOCKED = Peg(0.0, 0.0, 0.0, 0.0)
BACK = Peg(0.0, 0.0, -0.8, 0.0)
#--- DISPLAY INFO -------------------------------------------------------------
_screen = get_platform().get_default_display().get_default_screen()
WIDTH, HEIGHT = _screen.width*1.0 ,_screen.height*1.0
ASPECT = WIDTH / HEIGHT
CENTX, CENTY = WIDTH*0.5, HEIGHT*0.5
SCREEN = (-CENTX, -CENTY, CENTX, CENTY)


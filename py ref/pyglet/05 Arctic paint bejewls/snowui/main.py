import rabbyt
from pyglet.event import EventDispatcher
from pyglet.window import mouse, key
from pyglet import window as pyglet_window
from pyglet.gl import *

import sys
sys.path.append("..")

from snowui.widget import Widget


class GUI(Widget, EventDispatcher):
    """
    ``GUI(**kwargs)``

    Creates a toplevel widget for event handling::

        gui = snowui.GUI()
        window.push_handlers(gui)
    """
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        EventDispatcher.__init__(self)
        if not self.bounds:
            self.bounds = "always"
        self.is_focused = True

    def blur(self):
        # We never want the gui widget to blur.
        pass




class Window(pyglet_window.Window):
    """
    ``Window([size, [fullscreen, [caption]]])``

    A simple wrapper around the pyglet window.
    """
    def __init__(self, size=(800,600), fullscreen=0, caption="snowui"):
        pyglet_window.Window.__init__(self, width=size[0], height=size[1])
        if fullscreen:
            self.set_fullscreen(True)

        self.set_caption(caption)
        rabbyt.set_default_attribs()


    def on_close(self):
        self.close()
        sys.exit()




class View(rabbyt.Animable):
    """
    ``View(window, [x, [y]])``

    A very usefull way to manage one or more cameras. Supports zooming, moving
    around, edge clamping and converting between onscreen coordinates to game
    coordinates. See examples in the example directory to see how it's used.

    ``x``, ``y`` and ``zoom`` are all ``rabbyt.anim_slot``s (you can assign a
    lerp to them).
    """
    zoom = rabbyt.anim_slot(1.0)
    x = rabbyt.anim_slot()
    y = rabbyt.anim_slot()

    def __init__(self, window, x=0, y=0):
        rabbyt.Animable.__init__(self)
        self.window = window
        self.x = x
        self.y = y
        self.zoom = 1.0
        self.width = window.width
        self.height = window.height

    def _set_xy(self, xy):
        self.x, self.y = xy

    xy = property(lambda self:(self.x,self.y), _set_xy)

    @property
    def scale_h(self):
        return self.window.height * self.zoom
    @property
    def scale_w(self):
        return self.window.width * self.zoom

    def to_world_pixels(self, (x,y), use_attrgetter=False):
        if use_attrgetter:
            sx = self.attrgetter("x")
            sy = self.attrgetter("y")
        else:
            sx,sy = self.xy
        return (sx+(x-self.width/2)*self.zoom,
                sy+(y-self.height/2)*self.zoom)

    def from_world_pixels(self, (x,y), use_attrgetter=False):
        if use_attrgetter:
            sx = self.attrgetter("x")
            sy = self.attrgetter("y")
        else:
            sx,sy = self.xy
        # FIXME: Needs to take into account zoom.
        return (x-(sx-self.width/2),
                y-(sy-self.height/2))

    @property
    def bounds(self):
        l = -self.width*self.zoom/2 + self.x
        t = self.height*self.zoom/2 + self.y
        r = self.width*self.zoom/2 + self.x
        b = -self.height*self.zoom/2 + self.y
        return (l, t, r, b)

    def keep_within(self, bounds):
        if self.bounds[0] < bounds[0]:
            self.x = bounds[0]+self.scale_w*.5
        if self.bounds[2] > bounds[2]:
            self.x = bounds[2]-self.scale_w*.5
        if self.bounds[2] >= bounds[2] and self.bounds[0] <= bounds[0]:
            self.x = (bounds[0] + bounds[2])*.5

        if self.bounds[3] < bounds[3]:
            self.y = bounds[3]+self.scale_h*.5
        if self.bounds[1] > bounds[1]:
            self.y = bounds[1]-self.scale_h*.5
        if self.bounds[1] >= bounds[1] and self.bounds[3] <= bounds[3]:
            self.y = (bounds[1] + bounds[3])*.5

    def set_viewport(self):
        l,t,r,b = self.bounds
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(l, r, b, t, -1000, 1000)
        glMatrixMode(GL_MODELVIEW)
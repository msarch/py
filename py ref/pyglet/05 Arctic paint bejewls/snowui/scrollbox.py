import rabbyt
from pyglet.window import mouse, key
from pyglet.gl import *
import ctypes

import sys
sys.path.append("..")

from snowui.widget import Widget


class Pan(Widget):
    def __init__(self, **kwargs):
        self.drag_button = None
        self.scroll_range_x = (0,0)
        self.scroll_range_y = (0,0)

        self.set_style("Pan", kwargs)
    
        Widget.__init__(self, **kwargs)
        self.bounds = "rect"

        # We assign ``rx`` and ``ry`` to get our scroll widget to use relative
        # positioning.
        self.scroll = Widget(bounds="always", rx=0, ry=0)
        Widget.add(self, self.scroll)

        self.add = self.scroll.add
        self.remove = self.scroll.remove

        self.__hovering = False
        self.__down = False


    def _scroll_range_x(self, r):
        self.scroll_range_x = r
    def _scroll_range_y(self, r):
        self.scroll_range_y = r

    def _drag_button(self, b):
        self.drag_button = b

    def on_mouse_motion(self, x, y, dx, dy):
        # We are overwriting on_mouse_motion instead of using
        # handle_mouse_motion becuase we only want to do it for children if it
        # collides with self.
        if self.collide((x,y)):
            self.__hovering = True
        else:
            if self.__hovering:
                for c in self.scroll.children:
                    c.do_blur()
                self.__hovering = True
                return

        self.handle_mouse_motion(x, y, dx, dy)
        for c in self.children:
            c.on_mouse_motion(x, y, dx, dy)

    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.drag_button and self.__down:
            if self.drag_button == buttons:
                self.scroll.rx = max(self.scroll_range_x[0],
                        min(self.scroll.rx+dx, self.scroll_range_x[1]))
                self.scroll.ry = max(self.scroll_range_y[0],
                        min(self.scroll.ry+dy, self.scroll_range_y[1]))
                return True
        return False


    def handle_mouse_press(self, x, y, button, modifiers):
        self.__down = True

    def handle_mouse_release(self, x, y, button, modifiers):
        self.__down = False


    def render(self):
        planes = (
                (ctypes.c_double*4)(-1.0, 0, 0.0, self.x+self.shape.width),
                (ctypes.c_double*4)(0, 2, 0.0, -self.y*2),
                (ctypes.c_double*4)(2, 0, 0.0, max(-self.x-self.shape.width,0)),
                (ctypes.c_double*4)(0, -1, 0.0, self.y+self.shape.height),
                )
        enums = [GL_CLIP_PLANE1, GL_CLIP_PLANE2, GL_CLIP_PLANE3, GL_CLIP_PLANE4]
        for i,p in enumerate(planes):
            glClipPlane(enums[i], p)
            glEnable(enums[i])
        Widget.render(self)
        for i,p in enumerate(planes):
            glDisable(enums[i])


class ScrollBox(Widget):
    def __init__(self, **kwargs):
        self.inwidgets = []

        self.set_style("ScrollBox", kwargs)

        Widget.__init__(self, **kwargs)
        self.bounds = "rect"

        nshape = rabbyt.Quad(self.shape)
        l = nshape.left
        nshape.width -= 20
        nshape.left = l
        self.pan = Pan(texture=self.get_style("ScrollBox.Pan"),
                shape=nshape, rx=0, ry=0)
        Widget.add(self, self.pan)

        self.scroll_bar = ScrollBar(pan_to_scroll=self.pan,
                texture=self.get_style("ScrollBox.ScrollBar"),
                shape=(0,self.shape.height,20,0),
                rx=self.shape.width-20, ry=0)
        Widget.add(self, self.scroll_bar)

    def add(self, w):
        self.pan.add(w)
        self.inwidgets.append(w)
        self.do_rearrange()

    def remove(self, w):
        self.pan.remove(w)
        self.inwidgets.remove(w)
        self.do_rearrange()

    def do_rearrange(self):
        content_height = 0
        for i,w in enumerate(self.inwidgets):
            content_height += w.shape.height
            w.rx = 0
            w.ry = self.pan.shape.height-content_height

        scroll_range = max(content_height-self.pan.shape.height, 0)
        self.pan.scroll_range_y = (0, scroll_range)



class ScrollBar(Pan):
    def __init__(self, pan_to_scroll, **kwargs):
        self.pan_to_scroll = pan_to_scroll

        self.set_style("ScrollBar", kwargs)

        Pan.__init__(self, drag_button=mouse.LEFT, **kwargs)
        self.scroll_range_y = (-self.shape.height+40,0)

        self.block = Widget(texture=self.get_style("ScrollBar.block"),
                shape=(0,40,20,0), rx=0,
                ry=self.shape.height-40)
        self.add(self.block)

    def handle_mouse_drag(self, *args):
        if Pan.handle_mouse_drag(self, *args):
            scroll_amount = abs(self.scroll.ry)
            scroll_range = abs(self.scroll_range_y[0])
            if scroll_range == 0:
                self.scroll.ry = 0
            else:
                r = scroll_amount/scroll_range
                self.pan_to_scroll.scroll.ry =\
                        self.pan_to_scroll.scroll_range_y[1]*r
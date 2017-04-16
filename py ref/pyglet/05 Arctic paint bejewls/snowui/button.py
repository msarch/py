import rabbyt
from pyglet.window import mouse, key

import sys
sys.path.append("..")

from snowui.widget import Widget


class Button(Widget):
    """
    ``Button(**kwargs)``

    A simple ``Widget`` with callback support and visual hover effects.

    Added options are:

        ``"icon"``
            Adds an icon to the button. The value should be a valid value for
            ``rabbyt.texture``.

        ``"callback"``
            A function that will be called when ever the button is pressed.

        ``"cb_data"``
            Extra data that can be passed with the callback.

        ``"hover_color"``
            The rgba color to fade to when the button is hovered. Defaults to
            (0.6, 0.6, 1, 1)

        ``"default_color"``
            The default rgba color for the button that it will fade back to when
            hovered out. Defaults to (1,1,1,1)

        ``"fade_time"``
            The time it takes to fade in or out. Defaults to 0.25
    """
    def __init__(self, **kwargs):
        self.hover_color = (0.6, 0.6, 1, 1)
        self.default_color = 1,1,1,1
        self.icon = None
        self.__callback = None
        self.is_hovering = False
        self.fade_time = .25

        self.set_style("Button", kwargs)

        Widget.__init__(self, **kwargs)

    def handle_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            if self.__callback:
                if hasattr(self, "cb_data"):
                    self.__callback(self.cb_data)
                else:
                    self.__callback()

    def _icon(self, icon):
        self.icon = Widget(texture=icon, shape=self.shape)
        self.icon.xy = self.attrgetter("xy")
        self.icon.alpha = self.attrgetter("alpha")
        self.icon.scale_x = self.attrgetter("scale_x")
        self.icon.scale_y = self.attrgetter("scale_y")
        self.add(self.icon)

    def _callback(self, cb):
        self.__callback = cb

    def _cb_data(self, d):
        self.cb_data = d

    def _hover_color(self, color):
        self.hover_color = color

    def _default_color(self, color):
        self.default_color = self.rgba = color

    def _fade_time(self, t):
        self.fade_time = t


    def do_fade(self, start_rgba, end_rgba):
        """
        ``do_fade(start_rgba, end_rgba)``

        Uses ``rabbyt.lerp`` to fade the button's color from ``start_rgba`` to
        ``end_rgba``.

        This is not meant to be called directly but is separated out here so you
        can overwrite it to easily have your own effects.
        """
        self.rgba = rabbyt.lerp(start=start_rgba, end=end_rgba,
                dt=self.fade_time)


    def handle_mouse_motion(self, x, y, dx=0, dy=0):
        if self.hover_color:
            if self.collide((x,y)):
                if not self.is_hovering:
                    self.do_fade(self.rgba, self.hover_color)
                    self.is_hovering = True
            elif self.is_hovering:
                self.do_fade(self.rgba, self.default_color)
                self.is_hovering = False


    def do_blur(self):
        Widget.do_blur(self)
        if self.is_hovering:
            self.do_fade(self.rgba, self.default_color)
            self.is_hovering = False

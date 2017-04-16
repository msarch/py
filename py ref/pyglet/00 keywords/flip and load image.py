import pyglet
from pyglet.gl import *
from math import radians, cos, sin, degrees, atan2
from time import time

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
pyglet.options['audio'] = ('alsa', 'openal', 'silent')
key = pyglet.window.key

class GUI(pyglet.window.Window):
    def __init__(self):
        super(GUI, self).__init__(640,340, caption='My app')
        self.alive = True
        self.keys_down = {}

        imgTexture = pyglet.image.load('/path/to/image.png')
        self.myImage = pyglet.sprite.Sprite(imgTexture)
        self.myImage.x, self.myImage.y = 10, 50 # x,y from bottom left corner

    def render(self, *args):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        # .. This is where you draw your objects, for instance
        self.myImage.draw()
        self.flip()

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = False

    def on_key_press(self, symbol, modkey):
        self.keys_down[symbol] = time()

    def on_key_release(self, symbol, modkey):
        if symbol in self.keys_down:
            del(self.keys_down[symbol])

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        print(button,'pressed',(x,y))


    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def run(self):
        while self.alive:
            event = self.dispatch_events()

            for symbol in self.keys_down:
                if symbol == key.ESCAPE:
                    self.alive = None
                    break
                elif symbol == key.LEFT:
                    pass #Arrowkey Left
                elif symbol == key.RIGHT:
                    pass #Arrowkey Right
                elif symbol == key.UP:
                    pass #Arrowkey Up
                elif symbol == key.DOWN:
                    pass #Arrowkey Down
                elif symbol == 65515:
                    pass # Win key
                else:
                    print(symbol)
            self.render()


if __name__ == '__main__':
    x = GUI()
    pyglet.clock.set_fps_limit(120)
    x.run()



##  IMPORTS -------------------------------------------------------------------
from pyglet import clock
import pyglet
from pyglet.gl import *
from pyglet.window import key


##--- WINDOW ------------------------------------------------------------------
class PygletViewport(pyglet.window.Window):

    def __init__(self,land):
        pyglet.window.Window.__init__(self,fullscreen=True)
        self.set_mouse_visible(False)
        self.land=land
        glClearColor(self.land.color[0],self.land.color[1],\
                self.land.color[2],self.land.color[3])
        #glClearColor(1.0, 1.0, 1.0, 1.0) # set background color to white
        glLoadIdentity() # reset transformation matrix
                # schedule the update function, 60 times per second
        clock.schedule_interval(self.update, 1.0/30.0)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            exit()
        elif symbol == key.P:
            self.land.paused = (True, False)[self.land.paused]

    def on_draw(self):
        """Clear the current OpenGL context, reset the model/view matrix and
        invoke the `draw()` methods of the renderers in order
        """
        if self.land.paused:
            # you may want to do something
            pass
        else:
            self.clear()
            self.land.draw()
            print 'FPS is %f' % clock.get_fps()

    def update(self,dt):
        if self.land.paused:
            # you may want to do something
            pass
        else:
            self.land.update(dt)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glClear(GL_STENCIL_BUFFER_BIT)
        glLoadIdentity()

#--- FUNCTIONS ----------------------------------------------------------------

def get_display_size():
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screen = display.get_default_screen()
    xmax = screen.width
    ymax = screen.height
    return(xmax,ymax)

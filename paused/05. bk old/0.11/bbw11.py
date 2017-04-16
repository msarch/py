#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# who : ms
# when : 07.2013
# what :  simple pyglet anim

# bbw11

import random, math
from pyglet import clock

import pyglet
from pyglet.gl import *
from pyglet.window import key


# create a batch to perform all our rendering
batch = pyglet.graphics.Batch()


##  CANVAS --------------------------------------------------------------------
class Canvas(pyglet.window.Window):

    def __init__(self):
        pyglet.window.Window.__init__(self,fullscreen=True)
        self.set_mouse_visible(False)
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        self.xmax = screen.width
        self.ymax = screen.height
        self.xc = (self.xmax*0.5)+1
        self.yc = (self.ymax*0.5)+1
        glClearColor(0.0, 0.0, 0.0, 0.0) # set background color to black
        #glClearColor(1.0, 1.0, 1.0, 1.0) # set background color to white
        glLoadIdentity() # reset transformation matrix
        glTranslatef(self.xc,self.yc,0.0)   # Move Origin to screen center
        self.frame=0
        self.list=[]
        batch.add(2, GL_LINES, None, ('v2i', (0,200, 800,300)))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:exit()

    def on_draw(self):
        self.clear()
        batch.draw()

    def append(self, tribe):
        self.list.append(tribe)

    def remove(self, tribe):
        self.list.remove(tribe)

    def clear(self):
        """ Clears the previous frame from the canvas.
        """
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glClear(GL_STENCIL_BUFFER_BIT)

    def run(self, draw=None, setup=None, update=None, stop=None):
        """ Opens the application windows and starts drawing the canvas.
        """
        pyglet.app.run()

    def update(self,dt):
        """ Updates the canvas and its tribes.
            This method does not actually draw anything, it only updates the state.
        """
        # Advance the animation by updating all tribes.
        self.frame += 1
        for tribe in self.list:tribe.update(dt)

    def render(self):
        """ Returns a screenshot of the current frame as a texture.
            This texture can be passed to the image() command.
        """
        return pyglet.image.get_buffer_manager().get_color_buffer().get_texture()

    def save(self, path):
        """ Exports the current frame as a PNG-file.
        """
        pyglet.image.get_buffer_manager().get_color_buffer().save(path)



# Ball is subclassed from Sprite, to ease drawin
class Ball(pyglet.sprite.Sprite):
    def __init__(self):
        pattern = pyglet.image.SolidColorImagePattern((255, 255, 255, 255))

        image = pyglet.image.create(8, 8, pattern)
        image.anchor_x, image.anchor_y = 4, 4

        pyglet.sprite.Sprite.__init__(self, image, batch=batch)

        self.x, self.y = 400, 250

        # give ourselves a random direction within 45 degrees of either paddle
        angle = random.random()*math.pi/2 + random.choice([-math.pi/4, 3*math.pi/4])
        # convert that direction into a velocity
        self.vx, self.vy = math.cos(angle)*300, math.sin(angle)*300

    def update(self, dt):
        # move the ball according to simple physics
        self.x += self.vx * dt
        self.y += self.vy * dt

        # reflect the ball if is in contact with the top of the playing area
        if self.y > 500-4:
            self.y = 500-4
            self.vy = -self.vy
        # and the same for the bottom
        elif self.y < 4:
            self.y = 4
            self.vy = -self.vy

        # reflect the ball right
        if self.x > 800-8:
            self.x = 800-8
            self.vx = -self.vx
        # change the velocity based on the distance to the center of the paddle

        #  left
        elif self.x < 8:
            self.x = 8
            self.vx = -self.vx

## CLASS TRIBE ----------------------------------------------------------------
class Tribe(list):

    def __init__(self,**kwargs):
        """ Creates a new tribe that can be appended to the canvas.
        """

    def update(self,dt):
        """Override this method to provide custom updating code.
        """
        pass

    def draw(self):
        """Override this method to provide custom drawing code.
        """
        pass

    def render(self):
        """Override this method to provide custom drawing code.
        """
        pass

##  C TRIBES ------------------------------------------------------------------
class running_squares_squadron(Tribe):
    def __init__(self):
        # add the ball
        b1 = Ball()
        b2 = Ball()
        self.append(b1)
        self.append(b2)
#        self.extend([b1,b2]) #.extend: add multiple elements,.append: add one
    def update(self, dt):
        for child in self: child.update(dt)



##  MAIN ----------------------------------------------------------------------
def main():
    c = Canvas()
    t1=running_squares_squadron()
    c.append(t1)

# schedule the update function, 60 times per second
    pyglet.clock.schedule_interval(c.update, 1.0/60.0)

# run the application
    c.run()


##  ---------------------------------------------------------------------------
if __name__ == "__main__": main()
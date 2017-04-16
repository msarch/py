import pyglet

import random
import math

import squirtle

class SkyDemo(object):
  """A simple demo of the Squirtle SVG mini-library.
  
  """
  def __init__(self):
    self.win = pyglet.window.Window(800, 600)
    self.win.push_handlers(self)

    squirtle.setup_gl() #Sets up blending so we get anti-aliased edges.

    self.sky = squirtle.SVG("svgs/sky.svg") #Anchors default to bottom left
    self.sun = squirtle.SVG("svgs/sun.svg", anchor_x='center', anchor_y='center')
    self.cloud = squirtle.SVG("svgs/cloud.svg", anchor_x='right', anchor_y='top')

    self.cloud_locs = [(random.uniform(0, 928), random.uniform(0, 728), random.uniform(1, 2)) for n in xrange(10)]
    self.cloud_locs = sorted(self.cloud_locs, key=lambda x: x[2])

    self.time_elapsed = 0
    self.fps = pyglet.clock.ClockDisplay()

    pyglet.clock.schedule_interval(self.tick, 1/60.0)
    pyglet.app.run()

  def tick(self, dt):
    self.cloud_locs = [((loc[0] + 50*dt) % 928, loc[1], loc[2]) for loc in self.cloud_locs]
    self.time_elapsed += dt

  def on_draw(self):
    self.win.clear()
    self.sky.draw(0, 0)
    self.sun.draw(600, 500, angle=10 * math.sin(self.time_elapsed))
    for x,y,z in self.cloud_locs:
      self.cloud.draw(x*z, y*z, scale=z)
    self.fps.draw()

if __name__ == '__main__':
  SkyDemo()
  
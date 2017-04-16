#
#This adds a square every time you press Space,
#and then pressing alpha keys will remove the squares you added. This works exactly as expected when deleting from the end, but not when removing from any earlier in the batch.
#Eg, generate five squares: 


import pyglet

window = pyglet.window.Window()
batch = pyglet.graphics.Batch()
polys = dict()
counter = 0

def add_poly(keycode, points):
   vertex_list = batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                                   (0, 1, 2, 0, 2, 3),
                                   ('v2f', points),
                                   ('c3f', (1, 1, 1) * 4))
   polys[keycode] = vertex_list

def poly(counter):
   min_x = 50 + (counter % 10)*50
   max_x = min_x + 35
   min_y = 50 + (counter/10)*50
   max_y = min_y + 35
   return (min_x, min_y, min_x, max_y, max_x, max_y, max_x, min_y)

@window.event
def on_draw():
   window.clear()
   batch.draw()

@window.event
def on_key_press(keycode, _):
   global polys
   if keycode == pyglet.window.key.SPACE:
      global counter
      add_poly(counter + pyglet.window.key.A, poly(counter))
      counter += 1
   if keycode in polys:
      polys[keycode].delete()
      del polys[keycode]

pyglet.app.run()
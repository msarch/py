import pyglet

config = pyglet.gl.Config(sample_buffers=1, samples=4,
                      depth_size=16, double_buffer=True)
window = pyglet.window.Window(resizable=True, config=config, vsync=True)

# create vertex data
num_verts = 4
side_length = 1.0
half_side = side_length / 2.0

# vertex positions of a square centered at the origin,
# ordered counter-clockwise, starting at lower right corner
vertex_positions = [ half_side,  -half_side,
                     half_side,   half_side,
                    -half_side,   half_side,
                    -half_side,  -half_side]

# six pairs of texture coords, one pair (u,v) for each vertex
# of each triangle
texture_coords = [1.0, 0.0,
                  1.0, 1.0,
                  0.0, 1.0,
                  0.0, 0.0]

# indices of the two triangles that make the square
# counter-clockwise orientation
triangle_indices = [0, 1, 2,
                    2, 3, 0]

# use indexed vertex list
vertex_array = pyglet.graphics.vertex_list_indexed(num_verts,
                                                   triangle_indices,
                                                   ('v2f', vertex_positions),
                                                   ('t2f', texture_coords))

# enable face culling, depth testing
pyglet.gl.glEnable(pyglet.gl.GL_CULL_FACE)
pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)

# texture set up
pic = pyglet.image.load('test.png')
texture = pic.get_texture()
pyglet.gl.glEnable(texture.target)
pyglet.gl.glBindTexture(texture.target, texture.id)

# set modelview matrix
pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
pyglet.gl.glLoadIdentity()
pyglet.gl.gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

@window.event
def on_resize(width, height):
    pyglet.gl.glViewport(0, 0, width, height)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.gluPerspective(45.0, width / float(height), 1.0, 100.0)
    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
    window.clear()
    vertex_array.draw(pyglet.gl.GL_TRIANGLES)

pyglet.app.run()

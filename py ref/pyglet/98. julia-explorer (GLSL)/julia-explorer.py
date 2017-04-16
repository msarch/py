import pyglet
from pyglet.gl import *
from shader import Shader



class JuliaWindow(pyglet.window.Window):
	def __init__(self):
		super(JuliaWindow, self).__init__(caption = 'julia', width = 512, height = 512)

		self.C = (-0.70176, -0.3842)

		shader_path = 'julia'
		self.shader = Shader(''.join(open('%s.v.glsl' % shader_path)), ''.join(open('%s.f.glsl' % shader_path)))

	def on_mouse_motion(self, x, y, dx, dy):
		self.C = (6. * ((float(x) / window.width) - .5), 6 * ((float(y) / window.height) - .5))

	def on_draw(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-1., 1., 1., -1., 0., 1.)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		self.shader.bind()
		self.shader.uniformf('C', *self.C)

		glBegin(GL_QUADS)
		glVertex2i(-1, -1)
		glTexCoord2i(-2, -2)
		glVertex2f(1, -1)
		glTexCoord2i(2, -2)
		glVertex2i(1,  1)
		glTexCoord2i(2, 2)
		glVertex2i(-1,  1)
		glTexCoord2i(-2, 2)
		glEnd()
		self.shader.unbind()


window = JuliaWindow()
pyglet.app.run()

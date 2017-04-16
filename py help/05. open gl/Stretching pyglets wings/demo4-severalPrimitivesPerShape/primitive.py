from pyglet.gl import GL_TRIANGLE_FAN

class Primitive(object):
    "Stores a single list of vertices and a color"

    def __init__(self, verts, color, primtype=GL_TRIANGLE_FAN):
        self.verts = verts
        self.color = color
        self.primtype = primtype

    def offset(self, dx, dy):
        self.verts = [(v[0] + dx, v[1] + dy) for v in self.verts]
        return self


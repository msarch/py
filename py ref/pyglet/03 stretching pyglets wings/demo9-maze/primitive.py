from pyglet.gl import GL_TRIANGLE_STRIP
from vertexutils import offset

class Primitive(object):
    """
    Stores a list of vertices, a single color, and a primitive type
    Intended to be rendered as a single OpenGL primitive
    """
    def __init__(self, verts, color, primtype=GL_TRIANGLE_STRIP):
        self.verts = verts
        self.color = color
        self.primtype = primtype

    def offset(self, dx, dy):
        newverts = offset(self.verts, dx, dy)
        return Primitive(newverts, self.color, primtype=self.primtype)


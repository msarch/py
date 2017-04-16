import pyglet
from pyglet.graphics import Batch
from math import sin,cos
from pyglet.gl import (
      glPopMatrix, glPushMatrix, glRotatef, glTranslatef)

from pyglet.gl import GL_TRIANGLE_STRIP

class Color(object):
    orange = (255, 127, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    red = (200, 0, 0)
    blue = (127, 127, 255)
    pink = (255, 187, 187)

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
        newverts = []
        for i in range(0, len(self.verts), 2):
            newverts += [self.verts[i]+dx,self.verts[i+1]+dy]
        return Primitive(newverts, self.color, primtype=self.primtype)

    def rotate(self, angle):
        newverts = []
        angle = -angle # no idea
        for i in range(0, len(self.verts), 2):
            x, y = self.verts[i], self.verts[i+1]
            newverts += [
                x * cos(angle) - y * sin(angle),
                y * cos(angle) + x * sin(angle) ]
        return Primitive(newverts, self.color, primtype=self.primtype)


P=Primitive

class Shape(object):
    "A list of primitives. Creates a single batch to draw these primitives."

    def __init__(self, items=None):
        self.primitives = []
        if items:
            self.add_items(items)
        self.batch = None

    def add_items(self, items):
        "'items' may contain primitives and/or shapes"
        for item in items:
            if isinstance(item, Shape):
                for prim in item.primitives:
                    self.primitives.append(prim)
            else:
                self.primitives.append(item)

    def get_batch(self):
        if self.batch is None:
            self.batch = Batch()
            for primitive in self.primitives:
                batchVerts = \
                    [primitive.verts[0], primitive.verts[1]] + \
                    primitive.verts + \
                    [primitive.verts[-2], primitive.verts[-1]]
                numverts = len(batchVerts) / 2
                self.batch.add(
                    numverts,
                    primitive.primtype,
                    None, # group
                    ('v2f/static', batchVerts),
                    ('c3B/static', primitive.color * numverts),
                    )
        return self.batch



def Rect(x,y,w=100,h=100):
    """ (basepoint x,basepoint y), width, height,color,offset
    v2                             v3
      +---------------------------+
      |                           |
      |                           |
      +---------------------------+
    vO                             v1

    glBegin(GL_TRIANGLE_STRIP);
    glVertex3fv(v0);
    glVertex3fv(v1);
    glVertex3fv(v2);
    glVertex3fv(v3);
    glEnd();
    """

    return [x,y,x+w,y,x,y+h,x+w,y+h]


egg_white = [
    -10, -25,
    -20, -15,
    +10, -25,
    -20, +15,
    +20, -15,
    -10, +25,
    +20, +15,
    +10, +25,
]
egg_yellow = [
    -10, -10,
    -10, +10,
    +10, -10,
    +10, +10,
]

creature = Shape([
    P(egg_white, Color.white).offset(+2, +1.5),
    P(egg_yellow, Color.orange).offset(+10, +2),
    P(Rect(100,100,w=120,h=200), Color.red).offset(100,-200),
    P(Rect(100,100,w=120,h=200), Color.red).rotate(10).offset(200,20)
])








window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()

 #   maze.shape.get_batch().draw()

    glPushMatrix()
    glTranslatef(200, 200, 0)
    glRotatef(0, 0, 0, 1)
    creature.get_batch().draw()
    glPopMatrix()

pyglet.app.run()





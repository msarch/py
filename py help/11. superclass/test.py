









from collections import OrderedDict


class Shape(object):
    """
    Stores a list of vertices, a single color, and a primitive type
    Intended to be rendered as a single OpenGL primitive
    """
    set = OrderedDict()

    def __init__(self, name, **kwargs):
        if name in self.__class__.set:
            raise ValueError('duplicate shape name', name)
            exit(1)
        else:
            self.name=name
            self.__class__.set[self.name] = self

        for i in kwargs:
            setattr(self,i,kwargs[i])

        self.build()
        self.flat_verts = None
        self.batch = None


class Blip(Shape):
    """
    Point, autocad style,
    color=color
    """
    def build(self):
        if not hasattr(self,'color'):
            self.color = (0,0,0,0)
        self.verts = [(-5,0),(5,0),(0,0),(0,5),(0,-5)]

class Rect(Shape):
    """
    Rectangle, lower left basepoint is @ origin
    w=width, h=height, color=color
    """

    def build(self):
        if not hasattr(self,'color'):
            self.color = (0,0,0,0)
        if not hasattr(self,'w'):
            self.w = 100
        if not hasattr(self,'h'):
            self.h = 50

        self.verts = [(0, 0),(self.w, 0),(0, self.h),(self.w, self.h)]

        # 2--------3
        # |        |
        # 0--------1


Blip('b1')
Rect('b1', color=(0,1,1,1), w=100, h=300) # or just p2 if p1 = 0

print Shape.set
for r in Shape.set: print r, Shape.set[r]

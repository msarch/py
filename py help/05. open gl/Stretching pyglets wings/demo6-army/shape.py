from itertools import chain
from pyglet.graphics import Batch

class Shape(object):
    "A list of primitives"

    def __init__(self, items=None):
        self.primitives = []
        if items:
            self.add_items(items)
        self.batch = None

    def add_items(self, items):
        "Add a list containing primitives and shapes"
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
                flatverts = primitive.get_flat_verts()
                numverts = len(flatverts) / 2
                self.batch.add(
                    numverts,
                    primitive.primtype,
                    None,
                    ('v2f/static', flatverts),
                    ('c3B/static', primitive.color * numverts)
                )
        return self.batch

    def offset(self, dx, dy):
        newprims = []
        for prim in self.primitives:
            newprims.append(prim.offset(dx, dy))
        return Shape(newprims)


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
        "Add a list of primitives and shapes"
        for item in items:
            if isinstance(item, Shape):
                self.add_shape(item)
            else:
                self.primitives.append(item)

    def add_shape(self, other):
        "Add the primitives from a given shape"
        for prim in other.primitives:
            self.primitives.append(prim)

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


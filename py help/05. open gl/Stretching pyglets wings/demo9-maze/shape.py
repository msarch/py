from pyglet.graphics import Batch

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

    def offset(self, dx, dy):
        newprims = []
        for prim in self.primitives:
            newprims.append(prim.offset(dx, dy))
        return Shape(newprims)


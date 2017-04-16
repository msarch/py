
class Shape(object):
    "A list of primitives"

    def __init__(self, items=None):
        self.primitives = []
        if items:
            self.add_items(items)

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


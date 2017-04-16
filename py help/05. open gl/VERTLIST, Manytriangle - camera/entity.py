
class Entity(object):

    def __init__(self, verts, position=None, angle=0):
        self.verts = verts
        if position is None:
            position = (0, 0)
        self.x, self.y = position
        self.angle = angle


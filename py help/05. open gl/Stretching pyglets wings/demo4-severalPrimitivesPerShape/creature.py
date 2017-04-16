
class Creature(object):
    "Stores the world-coordinates and shape of a rendered object"

    def __init__(self, shape, position=None, angle=0):
        self.shape = shape
        if position is None:
            position = (0, 0)
        self.x, self.y = position
        self.angle = angle
        self.age = 0.0
        self.dx, self.dy = 0, 0

    def update(self, dt):
        self.age += dt
        self.x += self.dx
        self.y += self.dy


class Popup(Creature):

    def update(self, dt):
        Creature.update(self, dt)
        if self.age < 0.2:
            self.dy = +0.5
        elif self.age < 0.8:
            self.dy = 0.0
        elif self.age < 1.0:
            self.dy = -0.5

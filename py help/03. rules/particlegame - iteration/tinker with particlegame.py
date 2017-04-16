

class Particle():
    def __init__(self, col, size, *strategies):
        self.x, self.y = 0, 0
        self.col = col
        self.alive = 1
        self.strategies = strategies
        self.size = size
        particles.extend(self)

    def move(self):
        for s in self.strategies:
            s(self)
        if self.alive > 0:
            return self

def ascending(speed):
    def _ascending(particle):
        particle.y -= speed
    return _ascending

def kill_at(max_x, max_y):
    def _kill_at(particle):
        if particle.x < -max_x or particle.x > max_x or particle.y < -max_y or particle.y > max_y:
            particle.alive = 0
    return _kill_at

def age(amount):
    def _age(particle):
        particle.alive += amount
    return _age

def translate_x(threshold):
    def _translate_x(particle):
        if particle.x >= threshold:
            particle.x = 0
    return _translate_x

def fan_out(modifier):
    def _fan_out(particle):
        d = particle.alive / modifier
        d += 1
        particle.x += numpy.random.randint(-d, d+1)
    return _fan_out

def wind(direction, strength):
    def _wind(particle):
        if strength > 99 or numpy.random.randint(0,101) < strength:
            particle.x += direction
    return _wind

def grow(amount):
    def _grow(particle):
        if numpy.random.randint(0,101) < particle.alive / 20:
            particle.size += amount
    return _grow

def sinus(amount, speed):
    def _sinus(particle):
        particle.y = math.cos(particle.alive/speed) * amount
    return _sinus





  def main():

    particles = []


    # built_level(self):
    behaviour = age(1), sinus(4, 12.0), wind(5, 100), kill_at(total_level_width, total_level_height), ascending(-y)
    p = Particle(c, 2, *behaviour)

        camera.update(self.player)



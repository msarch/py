import math
import pyglet


window = pyglet.window.Window(width=sprite.width, height=sprite.height)

# Set window background color to white.
pyglet.gl.glClearColor(1, 1, 1, 1)

@window.event
def on_draw():
    window.clear()
    sprite.draw()

pyglet.app.run()


pygame.init()
screen = pygame.display.set_mode((400,400))

while True:
    t = pygame.time.get_ticks() / 2  % 400 # scale and loop time
    x = t
    y = math.sin(t/50.0) * 100 + 200       # scale sine wave
    y = int(y)                             # needs to be int

    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255,255,255), (x, y), 40)

    pygame.display.flip(  )

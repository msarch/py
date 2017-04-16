import pygame
from pygame.locals import *

class Cube(pygame.Surface):
    def __init__(self, width, height, depth, color):
        pygame.Surface.__init__(self, (width, height))
        self.depth = depth
        self.fill(Color(color))

def draw_cubes(cubes, screen):
    cubes_sorted = sorted(cubes, key=lambda cube: cube.depth, reverse=True)
    (x, y) = (180, 100)
    for cube in cubes_sorted:
        screen.blit(cube, (x, y))
        (x, y) = (x + 20, y + 20)

if __name__ == "__main__":
    cubes = [
        Cube(50, 50, 0, "red"),
        Cube(50, 50, 1, "green"),
        Cube(50, 50, 2, "blue")]

    screen = pygame.display.set_mode((480, 320))
    draw_cubes(cubes, screen)

    pygame.init()
    while 1:
        pygame.display.update()

"""
this example demonstrates how to find distance between polygons and implement
discrete collision detection using the distance method
"""



from operator import mul

from numpy import array
from pylygon import Polygon
import pygame
from pygame import display, draw, event, mouse, Surface
from pygame.font import Font
from pygame.locals import *



if __name__ == '__main__':
    pygame.init()

    SCREEN_SIZE = (800, 600)               # initialize screen size
    SCREEN = display.set_mode(SCREEN_SIZE) # load screen

    triangle = Polygon([(0, 70), (110, 0), (110, 70)])
    rhombus = Polygon([(0, 80), (20, 0), (80, 0), (60, 80)])

    triangle.move_ip(200, 200)
    rhombus.move_ip(300, 300)

    font = Font(None, 24)

    r = mouse.get_rel()
    grab, other = None, None
    while 1:
        SCREEN.fill((0, 0, 0))
        draw.polygon(SCREEN, (255, 0, 0), triangle.P, 1)
        draw.polygon(SCREEN, (0, 0, 255), rhombus.P, 1)
        mouse_pos = mouse.get_pos()
        for ev in event.get():
            if ev.type == KEYDOWN:
                if ev.key == K_q: exit()
            if ev.type == MOUSEBUTTONDOWN:
                if grab: grab, other = None, None
                elif rhombus.collidepoint(mouse_pos):
                    grab = rhombus
                    other = triangle
                elif triangle.collidepoint(mouse_pos):
                    grab = triangle
                    other = rhombus

        Y_triangle = triangle.project((0, 1))
        Y_rhombus = rhombus.project((0, 1))
        draw.line(SCREEN, (255, 0, 0), (2, Y_triangle[0]), (2, Y_triangle[1]), 2)
        draw.line(SCREEN, (0, 0, 255), (7, Y_rhombus[0]), (7, Y_rhombus[1]), 2)

        X_triangle = triangle.project((1, 0))
        X_rhombus = rhombus.project((1, 0))
        draw.line(SCREEN, (255, 0, 0), (X_triangle[0], 2), (X_triangle[1], 2), 2)
        draw.line(SCREEN, (0, 0, 255), (X_rhombus[0], 7), (X_rhombus[1], 7), 2)

        draw.circle(SCREEN, (255, 255, 255), triangle.C.astype(int), 3)
        draw.circle(SCREEN, (255, 255, 255), rhombus.C.astype(int), 3)

        r = array(mouse.get_rel())
        if grab:
            grab.C = mouse_pos
            distance = grab.distance(other, -r)
            msg = font.render(str(distance), 0, (255, 255, 255))
            SCREEN.blit(msg, (0, 0))

        display.update()

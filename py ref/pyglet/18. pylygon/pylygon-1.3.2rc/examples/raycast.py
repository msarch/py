"""
this example demonstrates how to implement continuous collision detection using
raycasting method
"""



from operator import mul

from numpy import array, dot
from pylygon import Polygon
import pygame
from pygame import display, draw, event, mouse, Surface
from pygame.locals import *



from numpy import seterr
seterr(divide='raise')



_prod = lambda X: reduce(mul, X)                        # product



if __name__ == '__main__':
    pygame.init()

    SCREEN_SIZE = (800, 600)               # initialize screen size
    SCREEN = display.set_mode(SCREEN_SIZE) # load screen

    triangle = Polygon([(0, 70), (110, 0), (110, 70)])
    rhombus = Polygon([(0, 80), (20, 0), (80, 0), (60, 80)])

    triangle.move_ip(200, 200)
    rhombus.move_ip(300, 300)

    grab, other, theta = None, None, 0
    while 1:
        SCREEN.fill((0, 0, 0))
        draw.polygon(SCREEN, (255, 0, 0), triangle.P, 1)
        draw.polygon(SCREEN, (0, 0, 255), rhombus.P, 1)
        mouse_pos = array(mouse.get_pos())
        for ev in event.get():
            if ev.type == KEYDOWN:
                if ev.key == K_q: exit()
                if ev.key == K_LEFT: theta = -0.01
                if ev.key == K_RIGHT: theta = 0.01
            if ev.type == KEYUP:
                if ev.key == K_LEFT: theta = 0
                if ev.key == K_RIGHT: theta = 0
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

        # NOTES on GJK:
        # ray r provided to the raycast algorithm must be towards the origin
        #   with respect to the movement direction; that is -r
        if grab:
            r = grab.C - mouse_pos # r is neg what mouse.get_rel() should return
            results = grab.raycast(other, r, self_theta = theta)
            if results:
                # if the objects are already intersecting, the results will be
                # zeros for everything.
                if results[0] == 0:
                    # use the hit normal to ensure the object is moving away
                    # from the intersection
                    if dot(r, n) > 0:
                        grab.move_ip(*-r)
                        # rotate?
                else:
                    lambda_, q, n = results
                    grab.move_ip(*-q)
                    grab.rotate_ip(lambda_ * theta)
            else:
                grab.move_ip(*-r)
                grab.rotate_ip(theta)

        display.update()

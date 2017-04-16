from shape import Shape
from primitive import Primitive

class Color(object):
    orange = (255, 127, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    yellow = (255, 255, 0)

eye_white = [
    (-1, -2.5),
    (-2, -1.5),
    (-2, +1.5),
    (-1, +2.5),
    (+1, +2.5),
    (+2, +1.5),
    (+2, -1.5),
    (+1, -2.5),
]
eye_pupil = [
    (-1, -1),
    (-1, +1),
    (+1, +1),
    (+1, -1),
]
eye_left = Shape([
    Primitive(eye_white, Color.white).offset(+2, +1.5),
    Primitive(eye_pupil, Color.black).offset(+1, +2)
])
eye_right = Shape([
    Primitive(eye_white, Color.white).offset(-4, +1.5),
    Primitive(eye_pupil, Color.black).offset(-5, +2)
])

ghost_body1 = [
    (-4.6, 5.3),
    (-2.9, 6.4),
    (-1.0, 6.9),
    (1.0, 6.9),
    (2.9, 6.4),
    (4.6, 5.3),
    (1, -5),
    (-1, -5),
]
ghost_body2 = [
    (4.6, 5.3),
    (5.9, 3.8),
    (6.7, 2.0),
    (7.0, 0.0),
    (7, -7),
    (5, -5),
    (3, -7),
    (1, -7),
    (1, -5),
]
ghost_body3 = [
    (-4.6, 5.3),
    (-1, -5),
    (-1, -7),
    (-3, -7),
    (-5, -5),
    (-7, -7),
    (-7.0, 0.0),
    (-6.7, 2.0),
    (-5.9, 3.8),
]

ghost = Shape([
    Primitive(ghost_body1, Color.orange),
    Primitive(ghost_body2, Color.orange),
    Primitive(ghost_body3, Color.orange),
    eye_left,
    eye_right,
])


pac_body = [
    (0, 0),
    (-6.7, 2.0),
    (-5.9, 3.8),
    (-4.6, 5.3),
    (-2.9, 6.4),
    (-1.0, 6.9),
    (1.0, 6.9),
    (2.9, 6.4),
    (4.6, 5.3),
    (5.9, 3.8),
    (6.7, 2.0),
    (7.0, 0.0),
    (6.7, -2.0),
    (5.9, -3.8),
    (4.6, -5.3),
    (2.9, -6.4),
    (1.0, -6.9),
    (-1.0, -6.9),
    (-2.9, -6.4),
    (-4.6, -5.3),
    (-5.9, -3.8),
    (-6.7, -2.0),
]

pacman = Shape([
    Primitive(pac_body, Color.yellow),
    Primitive(eye_pupil, Color.black).offset(0, +4),
])


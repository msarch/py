from shape import Shape
from primitive import Primitive

class Color(object):
    orange = (255, 127, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    red = (200, 0, 0)
    blue = (127, 127, 255)
    pink = (255, 187, 187)

eye_white = [
    (-1, -2.5),
    (-2, -1.5),
    (+1, -2.5),
    (-2, +1.5),
    (+2, -1.5),
    (-1, +2.5),
    (+2, +1.5),
    (+1, +2.5),
]
eye_pupil = [
    (-1, -1),
    (-1, +1),
    (+1, -1),
    (+1, +1),
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
    (-7, -7),   # 0
    (-7.0, 0.0),# 1
    (-5, -5),   # 22
    (-6.7, 2.0),# 2
    (-3, -7),   # 21
    (-5.9, 3.8),# 3
    (-1, -7),   # 20
    (-4.6, 5.3),# 4
    (-1, -5),   # 19
    (-2.9, 6.4),# 5
    (1, -5),    # 18
    (-1.0, 6.9),# 6
    (3, -7),    # 16
    (1.0, 6.9), # 7
    (5, -5),    # 15
    (2.9, 6.4), # 8
    (7, -7),    # 14
    (4.6, 5.3), # 9
    (7.0, 0.0), # 13
    (4.6, 5.3), # 10
    (6.7, 2.0), # 12
    (5.9, 3.8), # 11
]
ghost_body2 = [
    (3, -7),    # 16
    (1, -7),    # 17
    (1, -5),    # 18
]

orange_ghost = Shape([
    Primitive(ghost_body2, Color.orange),
    Primitive(ghost_body1, Color.orange),
    eye_left,
    eye_right,
])
orange_ghost.get_batch()
red_ghost = Shape([
    Primitive(ghost_body2, Color.red),
    Primitive(ghost_body1, Color.red),
    eye_left,
    eye_right,
])
red_ghost.get_batch()
blue_ghost = Shape([
    Primitive(ghost_body2, Color.blue),
    Primitive(ghost_body1, Color.blue),
    eye_left,
    eye_right,
])
blue_ghost.get_batch()
pink_ghost = Shape([
    Primitive(ghost_body2, Color.pink),
    Primitive(ghost_body1, Color.pink),
    eye_left,
    eye_right,
])
pink_ghost.get_batch()

pac_body1 = [
    (-6.7, 2.0),  # 1
    (0, 0),       # 0
    (-5.9, 3.8),  # 2
    (7.0, 0.0),   # 11
    (-4.6, 5.3),  # 3
    (6.7, 2.0),   # 10
    (-2.9, 6.4),  # 4
    (5.9, 3.8),   # 9
    (-1.0, 6.9),  # 5
    (4.6, 5.3),   # 8
    (1.0, 6.9),   # 6
    (2.9, 6.4),   # 7
]
pac_body2 = [
    (-6.7, -2.0), # 21
    (0, 0),       # 0
    (-5.9, -3.8), # 20
    (7.0, 0.0),   # 11
    (-4.6, -5.3), # 19
    (6.7, -2.0),  # 12
    (-2.9, -6.4), # 18
    (5.9, -3.8),  # 13
    (-1.0, -6.9), # 17
    (4.6, -5.3),  # 14
    (1.0, -6.9),  # 16
    (2.9, -6.4),  # 15
]

pacman = Shape([
    Primitive(pac_body1, Color.yellow),
    Primitive(pac_body2, Color.yellow),
    Primitive(eye_pupil, Color.black).offset(0, +4),
])

all_ghosts = [blue_ghost, orange_ghost, pink_ghost, red_ghost]

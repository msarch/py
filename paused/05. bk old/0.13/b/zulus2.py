#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# zululand :: zulus: :: rev 13-a :: 10.2013 :: msarch@free.fr

##  IMPORTS -------------------------------------------------------------------

##  CONSTANTS AND VARIABLES ---------------------------------------------------

##--- ZULUS CLASS -------------------------------------------------------------

class Zulu(object):
    """ Zulus objects themselves are merely identifiers of canvas entities.
    They do not contain any data themselves other than an entity id.
    Entities must be instantiated, constructor arguments can be
    specified arbitarily by the subclass.
    """


#--- ZULUS V2 -----------------------------------------------------------------


class Position(Component):
    """Predefined component that stores position and orientation info for
    entities.

    Fields:

    - **position** (Vec2d) -- Position vector
    - **angle** (float) -- Angle, in degrees
    """

    def __init__(self):
        Component.__init__(self, position=Vec2d, angle=float)


class Transform(Component):
    """Predefined component that stores offset, shear,
    rotation and scale info for entity shapes.

    Fields:

    - **offset** (Vec2d)
    - **shear** (Vec2d)
    - **rotation** (float)
    - **scale** (float, default 1.0)
    """

    def __init__(self):
        Component.__init__(self, offset=Vec2d, shear=Vec2d, rotation=float, scale=float)
        self.fields['scale'].default = lambda: 1.0


class Movement(Component):
    """Predefined component that stores velocity,
    acceleration and rotation info for entities.

    Fields:

    - **velocity** (Vec2d) -- Rate of change of entity position
    - **accel** (Vec2d) -- Rate of change of entity velocity
    - **rotation** (Vec2d) -- Rate of change of entity angle, in degrees/time
    """

    def __init__(self):
        Component.__init__(self, velocity=Vec2d, accel=Vec2d, rotation=float)


class Shape(Component):
    """Predefined component that stores shape vertices for entities

    - **closed** (bool) -- If the shapes is closed implying an edge between
      last and first vertices.
    - **verts** (Vec2dArray) -- Array of vertex points
    """

    def __init__(self):
        Component.__init__(self, closed=int, verts=Vec2dArray)
        self.fields['closed'].default = lambda: 1


class Renderable(Component):
    """Predefined component that identifies entities to be
    rendered and provides their depth and color.

    - **depth** (float) -- Drawing depth, can be used to determine z-order
          while rendering.
    - **color** (color.RGBA) -- Color used for entity. The effect of this
          field depends on the renderer.
    """

    def __init__(self):
        Component.__init__(self, depth=float, color=color.RGBA)
        self.fields['color'].default = lambda: color.RGBA(1)


#--- FUNCTIONS ----------------------------------------------------------------






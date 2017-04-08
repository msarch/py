#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# vim file
# do not delete folding markers : triple { and triple }
# zm to fold more (zM folds all)
# zr to reduce folding (zR reduces folding to none)

"""simple pyglet animation, ms, 10-2016 """

import color
import math
import pyglet
import pyglet.gl as GL
import squirtle

SVG = squirtle.SVG
SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 1280, 800, 60
PI, TWOPI = math.pi, math.pi * 2
SPEED = TWOPI / 2  # TWOPI/2 --> 1 engine revolution in 2 seconds
# BOW = pyglet.media.load('bow.wav', streaming=False)
# BOW1 = pyglet.media.load('bow1.wav', streaming=False)
# BOW.play()
'''
=== START OF ENGINE SECTION ===================================================
'''

##  CANVAS --------------------------------------------------------------------
class Canvas(pyglet.window.Window):
    """
    pyglet window
    running following sets, in that order: engines, actions, observers
    displaying : list of shapes
    """

    def __init__(self, w=SCREEN_WIDTH, h=SCREEN_HEIGHT, fps=FPS,
                 alpha=0, omega=SPEED):
        pyglet.window.Window.__init__(self, fullscreen=True)
        self.set_mouse_visible(False)
        self.w, self.h, self.fps = 1.0 * w, 1.0 * h, fps
        self.layers, self.actions, self.observers = [], [], []
        self.i_layers = []  # those layers visibility is toggled by key 'I'
        self.alpha, self.omega = alpha, omega  # start angle, angular velocity
        self.cosalpha = math.cos(-self.alpha)
        self.sinalpha = math.sin(-self.alpha)

        # camera stuff
        self.x, self.y = 0, 0
        self.scale = 100
        self.ratio = self.w / self.h
        self.target_x, self.target_y = self.x, self.y
        self.target_scale = self.scale

        self.setup_gl()
        pyglet.clock.schedule_interval(self.update, 1.0 / fps)

    def setup_gl(self):
        """Set various pieces of OpenGL state for better rendering of SVG.

        """
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glTranslatef(0.5 * self.w, 0.5 * self.h, 0.0)  #Origin:screen center
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)  # set background color to black

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
        elif symbol == pyglet.window.key.PAGEDOWN:
            self.camera_zoom(1.25)
        elif symbol == pyglet.window.key.PAGEUP:
            self.camera_zoom(0.8)
        elif symbol == pyglet.window.key.LEFT:
            self.camera_pan(self.scale / 2, 0)
        elif symbol == pyglet.window.key.RIGHT:
            self.camera_pan(-self.scale / 2, 0)
        elif symbol == pyglet.window.key.DOWN:
            self.camera_pan(0, self.scale / 2)
        elif symbol == pyglet.window.key.UP:
            self.camera_pan(0, -self.scale / 2)
        elif symbol == pyglet.window.key.I:
            for l in self.i_layers: l.visible = not l.visible


            # camera ----------------------------------------------------------
            # Camera stuff mostly from Jonathan Hartley (tartley@tartley.com)
            # demo's stretching pyglets wings

    def camera_zoom(self, factor):
        self.target_scale *= factor

    def camera_pan(self, dx, dy):
        self.target_x += dx
        self.target_y += dy

    def camera_update(self):  # update reaches target in ten times
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1
        self.scale += (self.target_scale - self.scale) * 0.1

    def camera_focus(self):
        "Set projection and modelview matrices ready for rendering"
        # Set projection matrix suitable for 2D rendering"
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        # GL.gluOrtho2D(left,right,bottom,top)
        GL.gluOrtho2D(
            -self.scale * self.ratio,
            self.scale * self.ratio,
            -self.scale,
            self.scale)
        # Set modelview matrix to move & scale to camera position"
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.gluLookAt(self.x, self.y, 1.0, self.x, self.y, -1.0, 0.0, 1.0, 0.0)

    # engine ------------------------------------------------------------------
    def engine_update(self, dt):
        """
        updates sine and cosine values in a uniform circular motion
        starting at angle : alpha
        angular velocity (per sec) : omega
        """
        self.alpha += dt * self.omega
        self.alpha = self.alpha % (TWOPI)  # stay within [0,2*Pi]
        # updates 2 coordinates with an harmonic linear osillation
        self.cosalpha = math.cos(self.alpha)
        self.sinalpha = math.sin(self.alpha)

    def draw(self):
        self.clear()
        self.camera_update()
        self.camera_focus()
        for l in self.layers: l.draw()

    def update(self, dt):
        self.engine_update(dt)
        for action in self.actions: action.update(dt)
        for observer in self.observers: observer.update(dt)
        self.draw()


    def run(self):
        pyglet.app.run()


# define the unique canvas now
canvas = Canvas()


##--- LAYER -------------------------------------------------------------------
# {{{
class Layer(object):
    """
    group of displayed elements
    """

    def __init__(self, pos=(0, 0), scale=1, angle=0, visible=True):
        self.pos, self.scale, self.angle = pos, scale, angle
        self.shapes = []
        self.visible = visible
        canvas.layers.append(self)

    def toggles(self):
        canvas.i_layers.append(self)

    def draw(self):
        if self.visible:
            GL.glPushMatrix()
            GL.glTranslatef(self.pos[0], self.pos[1], 0)
            GL.glScalef(self.scale, self.scale, 1)
            GL.glRotatef(self.angle, 0.0, 0.0, 1.0)
            for s in self.shapes:
                s.draw()  # * expands list (no append method)
            GL.glPopMatrix()

    def move(self, dx, dy):
        self.pos += (dx, dy)

    def rotate(self, alpha):
        self.angle += alpha

    def rescale(self, a):
        self.scale *= a


# define a default layer now
layer_0 = Layer()


##--- SHAPES ------------------------------------------------------------------
class Shape(object):
    """
    superclass for displayed elements
    """

    def __init__(self, layer=layer_0, color=color.red, **kwargs):
        self.layer = layer
        self.color = color
        self.setup(**kwargs)
        if not hasattr(self, 'pos'): self.pos = (0, 0)
        if not hasattr(self, 'vtx'): self.vtx = [-3, 0, 3, 0, 0, 0, 0, 3, 0, -3]
        # in this list vtx coordinates are flatened: [x0,y0,x1,y1,x2,y2...etc.]
        if not hasattr(self, 'glstring'): self.glstring = (5,
                pyglet.gl.GL_LINE_STRIP, None, ('v2i/static', self.vtx))
        if not hasattr(self, 'batch'): self.getbatch()
        self.layer.shapes.append(self)

    def getbatch(self):
        self.batch = pyglet.graphics.Batch()
        self.batch.add(*self.glstring)

    def draw(self):
        GL.glPushMatrix()
        GL.glTranslatef(self.pos[0], self.pos[1], 0)
        self.batch.draw()  # * expands list (no append method)
        GL.glPopMatrix()

    def translate(self, x, y):
        for i in xrange(0, len(self.vtx), 2):
            self.vtx[i] += x
            self.vtx[i + 1] += y
            self.getbatch()
        return (self)
        # don't forget to return self to be able to use short syntax
        #     sh=shape(...).tranlate(...)
        # rather than:
        #     sh=shape(....)
        #     sh.tranlate(...)

    # usually not used but will update batch if necessary
    # ie: in case positions of the end points of a Line are modified.
    def update(self, dt):
        self.getbatch()


class SVGshape(Shape):
    def setup(self,svg=None):
        self.svg = svg

    def draw(self):
        self.svg.draw(self.pos[0], self.pos[1], scale=1, angle=0)


class Point(Shape):
    """
    Simple Point, Autocad style cross
    """

    def setup(self):
        self.vtx = [-3, 0, 3, 0, 0, 0, 0, 3, 0, -3]
        self.glstring = (5, pyglet.gl.GL_LINE_STRIP, None, ('v2i/static',
            self.vtx),('c4B/static', self.color * 5))


class Line(Shape):
    """
    Simple line defined by 2 points
    """

    def setup(self, p1=Point(), p2=Point()):
        self.p1, self.p2 = p1, p2
        self.glstring = (2, pyglet.gl.GL_LINES, None,('v2f/static',
            (self.p1.pos[0], self.p1.pos[1], self.p2.pos[0], self.p2.pos[1])),
            ('c4B/static', self.color * 2))


class Rect(Shape):
    """
    Rectangle, orthogonal, FILED, origin is bottom left
    N,S,E,W = north, south east, west coordinates
      _N_
    W|___|E
       S
    """

    def setup(self, N=0, S=0, E=0, W=0):  # kapla default size
        self.vtx = [E, S, W, S, W, N, E, N]
        self.glstring = (4,
                pyglet.gl.GL_TRIANGLE_FAN,
                None,
                ('v2f/static', self.vtx),
                ('c4B/static', self.color * 4))


class Rect2(Shape):
    """
    Rectangle, orthogonal, OUTLINE ONLY, origin is bottom left
    """

    def setup(self, S=0, E=0, N=0, W=0):  # kapla default size
        self.vtx = [E, S, W, S, W, N, E, N, E, S]
        self.glstring = (5,
                pyglet.gl.GL_LINE_STRIP,
                None,
                ('v2f/static', self.vtx),
                ('c4B/static', self.color * 5))


class Circle(Shape):
    """
    Circle, outline only
    """

    def setup(self, radius=100, point=None):
        if point:
            self.radius = math.sqrt(point[0]**2+point[1]**2)
        else: self.radius = radius
        phi = 0
        stepangle = PI / (int(self.radius / 5) + 12)
        # number of divisions per ∏ rads (half the circle)
        # with vertices numbered like a clock,  GL_TRIANGLE_STRIP order is:
        # 11, 12, 10, 1, 9, 2, 8, 3, 7, 4, 6, 5
        self.vtx = [0, self.radius]  # create list and first element
        while phi < TWOPI:
            self.vtx.append(self.radius * math.sin(phi))
            self.vtx.append(self.radius * math.cos(phi))
            phi += stepangle
        self.vtx.extend([0, self.radius])  # add right side vertex
        n = int(len(self.vtx) / 2)
        self.glstring = (n,
                pyglet.gl.GL_LINE_STRIP,
                None,
                ('v2f/static',self.vtx),
                ('c4B/static', self.color * n))


##--- CROSSHAIR VERTICAL
class Vline(Shape):
    """
    fullscreen vertical line
    """

    def setup(self):
        self.vtx = [0, 0]  # x only
        self.glstring = (2,
                pyglet.gl.GL_LINES,
                None,
                ('v2f/static',
                (self.vtx[0], -SCREEN_HEIGHT, self.vtx[0], SCREEN_HEIGHT)),
                ('c4B/static', self.color * 2))


##--- CROSSHAIR HORIZONTAL
class Hline(Shape):
    """
    fullscreen horizontal line
    """

    def setup(self):
        self.vtx = [0, 0]
        self.glstring = (2,
                pyglet.gl.GL_LINES,
                None, ('v2f/static',
                (-SCREEN_WIDTH, self.vtx[1], SCREEN_WIDTH, self.vtx[1])),
                ('c4B/static', self.color * 2))


##--- ACTIONS -----------------------------------------------------------------

##--- HARMONIC OSILLATION
class Scotchyoke(object):
    """
    modifies target X or Y coordinate to match canvas circular motion generator
    """

    def __init__(self, target, Hradius=0, Vradius=0, center=(0, 0), direction=1, phase=0):
        self.target = target
        self.Hradius, self.Vradius = Hradius, Vradius
        self.dx, self.dy = center
        self.cosb, self.sinb = math.cos(phase) * direction, math.sin(phase)
        cosa, sina = canvas.cosalpha, canvas.sinalpha

    def update(self, dt):
        # cos(A+B)=cos A cos B - sin A sin B
        cosab = canvas.cosalpha * self.cosb - canvas.sinalpha * self.sinb
        # sin(A+B)=sin A cos B + cos A sin B
        sinab = canvas.sinalpha * self.cosb + canvas.cosalpha * self.sinb
        # set target position
        self.target.pos = (self.dx + cosab * self.Hradius, self.dy + sinab * self.Vradius)


##--- ROTATION
class SimpleRotation(object):
    """
    applies a continuous rotation to the target layer
    """
    RAD2DEG = 57.2957795131

    def __init__(self, target=None, center=(0, 0), phase=0):
        self.target, self.phase = target, phase
        self.target.pos += center

    def update(self, dt):
        self.target.angle = 57.2957795131 * (canvas.alpha + self.phase)
        # radians to degrees glRotate needs degrees !


##--- COLOR CYCLE
class ColorCycle(object):
    """
    applies in a circular way a list of colors to a list of objects
    """

    def __init__(self, target, colorset):
        self.target, self.colorset = target, colorset

    def update(self, dt):
        pass



##--- OBSERVERS ---------------------------------------------------------------

# --- CHANGE COLOR ON BOUNCE
class reverse_dir(object):
    """
    Checks for each axis if direction of target motion has changed
    """

    def __init__(self, target=None):
        self.target = target
        self.previous = self.target.pos
        self.dirx, self.diry = 0, 0

    def update(self, dt):
        newdirx = cmp(self.target.pos[0], self.previous[0])
        newdiry = cmp(self.target.pos[1], self.previous[1])
        if newdirx != self.dirx:
            self.dirx = newdirx
            #            BOW.play()

            print self.target, "reversed dir x"
        elif newdiry != self.diry:
            self.diry = newdiry
            #            BOW1.play()

            print self.target, "reversed dir y"
        else:
            pass


# }}}
##--- END OF OBSERVERSS -------------------------------------------------------

# }}}
'''
=== END OF ENGINE SECTION =====================================================
'''

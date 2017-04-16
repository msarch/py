
#
# Circle1D: A lame 2D "Physics" Engine <http://thp.io/2013/circle1d/>
# Copyright (c) 2013, Thomas Perl.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import math

class Vec2:
    # Two-dimensional vector

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vec2(self.x / scalar, self.y / scalar)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __eq__(self, other):
        return (self - other).length() < .0001

    def normalize(self):
        l = self.length()
        if l == 0:
            return Vec2(0, 0)
        return self / l

class Event:
    # Input event (pos is relative for DRAG, absolute otherwise)

    PRESS, RELEASE, DRAG = range(3)

    def __init__(self, type, pos):
        self.type = type
        self.pos = pos

class Object:
    # An object is a circle of a given size, and can optionally collide
    # with other objects. The position is influenced by external forces.

    NONE, COLLIDER, NOGRAVITY, FIXED = (1<<x for x in range(4))

    def __init__(self, scene, x, y, size, flags=NONE):
        self.scene = scene
        self.pos = Vec2(x, y)
        self.size = size
        self.flags = flags
        self.velocity = Vec2(0, 0)
        self.force = Vec2(0, 0)
        self.mouse = None
        self.mouse_joint = None
        self.compound = None

        self.scene.add_object(self)

    def handle(self, event):
        if event.type == Event.PRESS:
            if (self.pos - event.pos).length() < self.size:
                self.mouse = Object(self.scene, event.pos.x, event.pos.y, 10, Object.FIXED)
                self.mouse_joint = Joint(self.scene, self, self.mouse, Joint.STRONG)
                return True
        elif event.type == Event.DRAG:
            if self.mouse is not None:
                self.mouse.pos += event.pos
                return True
        elif event.type == Event.RELEASE:
            if self.mouse is not None:
                self.scene.remove_object(self.mouse)
                self.scene.remove_joint(self.mouse_joint)
                self.mouse = self.mouse_joint = None
                return True

        return False

    def simulate(self):
        # Estimated weight of object
        weight = self.size*self.size*3.

        # Gravity force
        if not (self.flags & (Object.NOGRAVITY | Object.FIXED)):
            self.force += Vec2(0, 16.2) * weight / 2000.

        # Force applies to velocity
        self.velocity += self.force / weight * 100.
        self.force = Vec2(0, 0)

        # Inertia and drag
        self.velocity *= .9

        # Actual movement of object based on current velocity
        self.pos += self.velocity

    def apply_force(self, direction):
        if not (self.flags & Object.FIXED):
            self.force += direction

    def move(self, destination):
        if not (self.flags & Object.FIXED):
            self.pos = destination

    @classmethod
    def handle_collisions(cls, objects):
        for i, a in enumerate(objects):
            for b in objects[i+1:]:
                if a.compound != b and b.compound != a:
                    a.handle_collision(b)

    def handle_collision(a, b): # a is self
        dist = (a.pos - b.pos)
        if (dist.x**2 + dist.y**2) < (a.size + b.size)**2:
            diff = (a.size + b.size) - dist.length()
            a_dir = (b.pos - a.pos).normalize()
            b_dir = dist.normalize()
            force = diff*.29*min(a.size, b.size)
            a.apply_force(b_dir*force)
            b.apply_force(a_dir*force)


class Joint:
    # A joint is a connection between two objects that maintains the
    # distance between the two objects, and can optionally break.

    NONE, RUBBERBAND, STRONG, BREAKABLE, BROKEN, FIXED = (1<<x for x in range(6))

    def __init__(self, scene, a, b, flags=NONE):
        self.scene = scene
        self.a = a
        self.b = b
        self.flags = flags

        # Initial distance of object is "ideal" distance of joint
        self.distance = (self.a.pos - self.b.pos).length()

        self.scene.add_joint(self)

    def simulate(self):
        # Broken joints are never simulated
        if self.flags & Joint.BROKEN:
            return

        # Check if current distance differs from "ideal" distance
        diff = self.distance - (self.a.pos - self.b.pos).length()
        if abs(diff) < 0.001:
            return

        # Breakable joints break when the distance difference is too big
        if (self.flags & Joint.BREAKABLE) and abs(diff) > abs(self.distance) * 4.:
            self.flags |= Joint.BROKEN
            return

        # Directional vector from A to B and from B to A
        a_dir = (self.b.pos - self.a.pos).normalize()
        b_dir = (self.a.pos - self.b.pos).normalize()

        # Fixed joints cause a direct movement of the objects (no forces)
        if self.flags & Joint.FIXED:
            if self.a.flags & Object.FIXED:
                self.b.move(self.a.pos + a_dir*self.distance)
            elif self.b.flags & Object.FIXED:
                self.a.move(self.b.pos + b_dir*self.distance)
            else:
                center = (self.a.pos + self.b.pos) / 2.
                self.a.move(center + b_dir*self.distance/2.)
                self.b.move(center + a_dir*self.distance/2.)
            return

        strength = abs(diff) * 2.
        if self.flags & Joint.RUBBERBAND:
            strength *= .2
        if self.flags & Joint.STRONG:
            strength *= 3.

        if diff < 0:
            # Attraction
            self.a.apply_force(a_dir*strength)
            self.b.apply_force(b_dir*strength)
        else:
            # Repulsion (not in case of rubberband-like joints)
            if not (self.flags & Joint.RUBBERBAND):
                self.a.apply_force(b_dir*strength)
                self.b.apply_force(a_dir*strength)

class Scene:
    # A scene manages a scene of objects and joints, and coordinates
    # simulation order and input event handling, as well as rendering

    def __init__(self, renderer):
        # All objects and the subset of collidable objects
        self.objects = []
        self.colliders = []

        # All joints and the subset of fixed joints
        self.joints = []
        self.fixed_joints = []

        self.renderer = renderer

    def add_object(self, o):
        self.objects.append(o)
        if o.flags & Object.COLLIDER:
            self.colliders.append(o)

    def remove_object(self, o):
        self.objects.remove(o)
        if o.flags & Object.COLLIDER:
            self.colliders.remove(o)

    def add_joint(self, j):
        self.joints.append(j)
        if j.flags & Joint.FIXED:
            self.fixed_joints.append(j)

    def remove_joint(self, j):
        self.joints.remove(j)
        if j.flags & Joint.FIXED:
            self.fixed_joints.remove(j)

    def render(self):
        # First, draw all objects as circles
        for o in self.objects:
            self.renderer.draw_circle(o.pos, o.size)

        # Then, draw all non-broken joints as lines
        for j in self.joints:
            if not (j.flags & Joint.BROKEN):
                self.renderer.draw_line(j.a.pos, j.b.pos)

    def handle(self, event):
        # Input events are handled only by objects
        for o in self.objects:
            if o.handle(event):
                break

    def simulate(self):
        # First we simulate the joints, so they apply forces on the objects
        for o in self.joints:
            o.simulate()

        # Then we simulate the objects which will process the applied forces
        for o in self.objects:
            o.simulate()

        # Fixed joints need additional iteration steps to better converge
        for i in range(10):
            for o in self.fixed_joints:
                o.simulate()

        # In the end, handle collisions (forces saved for next simulation step
        Object.handle_collisions(self.colliders)


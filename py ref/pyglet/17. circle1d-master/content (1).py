
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

from model import *

def scene_square(scene):
    radius = 60
    a = Object(scene, 10, 10, radius, Object.COLLIDER)
    b = Object(scene, 10, 150, radius, Object.COLLIDER)
    c = Object(scene, 150, 150, radius, Object.COLLIDER)
    d = Object(scene, 150, 10, radius, Object.COLLIDER)
    e = Object(scene, 80, 80, 130, Object.COLLIDER)
    a.compound = b.compound = c.compound = d.compound = e

    Joint(scene, a, b, Joint.FIXED)
    Joint(scene, b, c, Joint.FIXED)
    Joint(scene, c, d, Joint.FIXED)
    Joint(scene, d, a, Joint.FIXED)

    Joint(scene, a, c, Joint.FIXED)
    Joint(scene, b, d, Joint.FIXED)

    Joint(scene, a, e, Joint.FIXED)
    Joint(scene, b, e, Joint.FIXED)
    Joint(scene, c, e, Joint.FIXED)
    Joint(scene, d, e, Joint.FIXED)

def scene_floor(scene):
    for i in range(20):
        Object(scene, -50+i*30, 600, 20, Object.FIXED | Object.COLLIDER)

    for i in range(50):
        Object(scene, -50+(20+i)*30, 600-i*i, 20, Object.FIXED | Object.COLLIDER)

def scene_rubberband(scene):
    x = 200
    y = 20
    o = Object(scene, x, y, 20, Object.FIXED)
    for i in range(60):
        x += 25
        n = Object(scene, x, y, 15, (Object.NONE if i % 40 != 39 else Object.FIXED) | Object.COLLIDER)
        Joint(scene, o, n, Joint.BREAKABLE | Joint.STRONG | Joint.RUBBERBAND)
        o = n

    x = 400
    y = -500
    for i in range(60):
        x += 10
        if i % 20 == 19:
            x -= 10*9
            y += 30
        Object(scene, x, y, 15, Object.COLLIDER)

def scene_collision(scene):
    for i in range(4):
        Object(scene, 390+120*i, 400, 80, Object.FIXED | Object.COLLIDER)

    for i in range(3):
        Object(scene, 190+120*i, 700, 80, Object.FIXED | Object.COLLIDER)

    for i in range(3):
        Object(scene, 710+120*i, 700, 80, Object.FIXED | Object.COLLIDER)

    o = None
    for i in range(25):
        n = Object(scene, 190+40*i, 20+30*i, 10, Object.COLLIDER)
        if o is not None:
            Joint(scene, o, n, Joint.RUBBERBAND | Joint.BREAKABLE)
        o = n

def scene_bubbles(scene):
    for i in range(4):
        Object(scene, 390+120*i, 400+(i==1 or i==2)*60, 80, Object.FIXED | Object.COLLIDER)

    for i in range(5):
        Object(scene, 90+120*i, 700+(3-abs(3-i))*30, 80, Object.FIXED | Object.COLLIDER)

    for i in range(5):
        Object(scene, 710+120*i, 700+(3-abs(3-i))*30, 80, Object.FIXED | Object.COLLIDER)

    for i in range(130):
        Object(scene, 240+30*(i%20), 20+100*i//60, 15, Object.COLLIDER)

    Object(scene, 550, -200, 120, Object.COLLIDER)



/**
 *
 * Circle1D: A lame 2D "Physics" Engine <http://thp.io/2013/circle1d/>
 * Copyright (c) 2013, Thomas Perl.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 *    list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 **/


function C1DVec2(x, y) {
    this.x = x;
    this.y = y;
};

C1DVec2.prototype.add = function(other) {
    return new C1DVec2(this.x + other.x, this.y + other.y);
};

C1DVec2.prototype.sub = function(other) {
    return new C1DVec2(this.x - other.x, this.y - other.y);
};

C1DVec2.prototype.mul = function(scalar) {
    return new C1DVec2(this.x * scalar, this.y * scalar);
};

C1DVec2.prototype.div = function(scalar) {
    return new C1DVec2(this.x / scalar, this.y / scalar);
};

C1DVec2.prototype.length = function() {
    return Math.sqrt(this.x*this.x + this.y*this.y);
};

C1DVec2.prototype.equals = function(other) {
    return this.sub(other).length() < 0.0001;
};

C1DVec2.prototype.normalize = function() {
    var l = this.length();
    if (l == 0) {
        return new C1DVec2(0, 0);
    }
    return this.div(l);
};

function C1DEvent(type, pos) {
    this.type = type;
    this.pos = pos;
};

C1DEvent.PRESS = (1 << 0);
C1DEvent.RELEASE = (1 << 1);
C1DEvent.DRAG = (1 << 2);

function C1DObject(scene, x, y, size, flags) {
    this.scene = scene;
    this.pos = new C1DVec2(x, y);
    this.size = size;
    this.flags = flags;
    this.velocity = new C1DVec2(0, 0);
    this.force = new C1DVec2(0, 0);
    this.mouse = null;
    this.mouse_joint = null;
    this.compound = null;

    this.scene.add_object(this);
};

C1DObject.NONE = (1 << 0);
C1DObject.COLLIDER = (1 << 1);
C1DObject.NOGRAVITY = (1 << 2);
C1DObject.FIXED = (1 << 3);

C1DObject.prototype.handle = function(evt) {
    if (evt.type === C1DEvent.PRESS) {
        if (this.pos.sub(evt.pos).length() < this.size) {
            this.mouse = new C1DObject(this.scene, evt.pos.x, evt.pos.y, 10, C1DObject.FIXED);
            this.mouse_joint = new C1DJoint(this.scene, this, this.mouse, C1DJoint.STRONG);
            return true;
        }
    } else if (evt.type === C1DEvent.DRAG) {
        if (this.mouse !== null) {
            this.mouse.pos = this.mouse.pos.add(evt.pos);
            return true;
        }
    } else if (evt.type === C1DEvent.RELEASE) {
        if (this.mouse !== null) {
            this.scene.remove_object(this.mouse);
            this.scene.remove_joint(this.mouse_joint);
            this.mouse = this.mouse_joint = null;
        }
    }

    return false;
};

C1DObject.prototype.simulate = function() {
    var weight = this.size * this.size * 3.;

    if (!(this.flags & (C1DObject.NOGRAVITY | C1DObject.FIXED))) {
        this.force = this.force.add(new C1DVec2(0, 16.2).mul(weight/2000.));
    }

    this.velocity = this.velocity.add(this.force.div(weight).mul(100.));
    this.force = new C1DVec2(0, 0);

    this.velocity = this.velocity.mul(0.9);

    this.pos = this.pos.add(this.velocity);
};

C1DObject.prototype.apply_force = function(direction) {
    if (!(this.flags & C1DObject.FIXED)) {
        this.force = this.force.add(direction);
    }
};

C1DObject.prototype.move = function(destination) {
    if (!(this.flags & C1DObject.FIXED)) {
        this.pos = destination;
    }
};

C1DObject.handle_collisions = function(objects) {
    var i, j;
    for (i=0; i<objects.length; i++) {
        for (j=i+1; j<objects.length; j++) {
            var a = objects[i];
            var b = objects[j];
            if (a.compound !== b && b.compound !== a) {
                a.handle_collision(b);
            }
        }
    }
};

C1DObject.prototype.handle_collision = function(other) {
    var a = this;
    var b = other;
    var dist = a.pos.sub(b.pos);
    if ((dist.x*dist.x + dist.y*dist.y) < (a.size + b.size)*(a.size + b.size)) {
        var diff = (a.size + b.size) - dist.length();
        var a_dir = b.pos.sub(a.pos).normalize();
        var b_dir = dist.normalize();
        var force = diff*.29*Math.min(a.size, b.size);
        a.apply_force(b_dir.mul(force));
        b.apply_force(a_dir.mul(force));
    }
};

function C1DJoint(scene, a, b, flags) {
    this.scene = scene;
    this.a = a;
    this.b = b;
    this.flags = flags;

    this.distance = this.a.pos.sub(this.b.pos).length();

    this.scene.add_joint(this);
};

C1DJoint.NONE = (1 << 0);
C1DJoint.RUBBERBAND = (1 << 1);
C1DJoint.STRONG = (1 << 2);
C1DJoint.BREAKABLE = (1 << 3);
C1DJoint.BROKEN = (1 << 4);
C1DJoint.FIXED = (1 << 5);

C1DJoint.prototype.simulate = function() {
    if (this.flags & C1DJoint.BROKEN) {
        return;
    }

    var diff = this.distance - this.a.pos.sub(this.b.pos).length();
    if (Math.abs(diff) < 0.001) {
        return;
    }

    if ((this.flags & C1DJoint.BREAKABLE) && Math.abs(diff) > Math.abs(this.distance) * 4.) {
        this.flags |= C1DJoint.BROKEN;
        return;
    }

    var a_dir = this.b.pos.sub(this.a.pos).normalize();
    var b_dir = this.a.pos.sub(this.b.pos).normalize();

    if (this.flags & C1DJoint.FIXED) {
        if (this.a.flags & C1DObject.FIXED) {
            this.b.move(this.a.pos.add(a_dir.mul(this.distance)));
        } else if (this.b.flags & C1DObject.FIXED) {
            this.a.move(this.b.pos.add(b_dir.mul(this.distance)));
        } else {
            var center = this.a.pos.add(this.b.pos).div(2.);
            this.a.move(center.add(b_dir.mul(this.distance/2.)));
            this.b.move(center.add(a_dir.mul(this.distance/2.)));
        }
        return;
    }

    var strength = Math.abs(diff) * 2.;
    if (this.flags & C1DJoint.RUBBERBAND) {
        strength = strength * .2;
    }
    if (this.flags & C1DJoint.STRONG) {
        strength = strength * 3.;
    }

    if (diff < 0) {
        this.a.apply_force(a_dir.mul(strength));
        this.b.apply_force(b_dir.mul(strength));
    } else {
        if (!(this.flags & C1DJoint.RUBBERBAND)) {
            this.a.apply_force(b_dir.mul(strength));
            this.b.apply_force(a_dir.mul(strength));
        }
    }
};


function C1DScene(renderer) {
    this.objects = [];
    this.colliders = [];

    this.joints = [];
    this.fixed_joints = [];

    this.renderer = renderer;
};

C1DScene.prototype.add_object = function(o) {
    this.objects.push(o);
    if (o.flags & C1DObject.COLLIDER) {
        this.colliders.push(o);
    }
};

C1DScene.prototype.remove_object = function(o) {
    this.objects.splice(this.objects.indexOf(o));
    if (o.flags & C1DObject.COLLIDER) {
        this.colliders.splice(this.colliders.indexOf(o));
    }
};

C1DScene.prototype.add_joint = function(j) {
    this.joints.push(j);
    if (j.flags & C1DJoint.FIXED) {
        this.fixed_joints.push(j);
    }
};

C1DScene.prototype.remove_joint = function(j) {
    this.joints.splice(this.joints.indexOf(j));
    if (j.flags & C1DJoint.FIXED) {
        this.fixed_joints.splice(this.fixed_joints.indexOf(j));
    }
};

C1DScene.prototype.render = function() {
    var that = this;
    this.objects.forEach(function (o) {
        that.renderer.draw_circle(o.pos, o.size);
    });
    this.joints.forEach(function (j) {
        if (!(j.flags & C1DJoint.BROKEN)) {
            that.renderer.draw_line(j.a.pos, j.b.pos);
        }
    });
};

C1DScene.prototype.handle = function(evt) {
    var i;
    for (i=0; i<this.objects.length; i++) {
        if (this.objects[i].handle(evt)) {
            break;
        }
    }
};

C1DScene.prototype.simulate = function() {
    this.joints.forEach(function (o) { o.simulate(); });

    this.objects.forEach(function (o) { o.simulate(); });

    for (var i=0; i<10; i++) {
        this.fixed_joints.forEach(function (o) { o.simulate(); });
    }

    C1DObject.handle_collisions(this.colliders);
};


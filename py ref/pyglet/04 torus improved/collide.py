#!/usr/bin/env python

'''
Mostly hacked up stuff that's missing from euclid.
Author: Alex Holkner
Alex.Holkner@mail.google.com
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import math
import operator

import euclid
import obj

class ConvexPolygon(object):
    __slots__ = ['plane', 'edge_planes', 'point', 'aabbox']

    def __init__(self, points):
        assert len(points) >= 3
        assert reduce(operator.and_, 
                      [isinstance(p, euclid.Point3) for p in points])
        self.plane = euclid.Plane(points[0], points[1], points[2])
        n = self.plane.n
        self.edge_planes = [ \
            euclid.Plane(p1, (p2 - p1).cross(n)) \
            for p1, p2 in map(None, points[:], points[1:] + [points[0]])
            if (p2 - p1).cross(n)] # Filter out edges that are colinear with
                                   # normal (non-planar polygon)

        self.point = points[0]     # An arbitrary point on this polygon

        # Axis aligned bounding box
        p1 = points[0].copy()
        p2 = points[0].copy()
        for p in points[1:]:
            if p.x < p1.x:
                p1.x = p.x
            if p.y < p1.y:
                p1.y = p.y
            if p.z < p1.z:
                p1.z = p.z
            if p.x > p2.x:
                p2.x = p.x
            if p.y > p2.y:
                p2.y = p.y
            if p.z > p2.z:
                p2.z = p.z
        self.aabbox = p1, p2

    def contact_ellipsoid(self, ellipsoid):
        '''Return penetration of ellipsoid through plane along plane normal
        or None if no collision.'''
        c = ellipsoid.c
        d = c.dot(self.plane.n) - self.plane.k
        r = abs(self.plane.n * ellipsoid.v)
        if abs(d) > r:
            return None

        # An approximation only, is a little too sensitive near the vertices
        # (collision planes extend infinitely and edge radius calculated
        # wrong).  Far cheaper than the exact solution though.
        
        # Get (squared) distance ellipsoid needs to be from edge plane (sphere
        # equation -- how wrong is this??) XXX 
        edge_r2 = r ** 2 - d ** 2
        for edge in self.edge_planes:
            dd = c.dot(edge.n) - edge.k 
            sd = dd / abs(dd) # Keep sign after squaring (optimising away sqrt)
            if sd * dd ** 2 > edge_r2:
                return None

        return r - d

    def intersect_line3(self, line):
        p = self.plane.intersect(line)
        if p is None:
            return None
        for edge in self.edge_planes:
            d = p.dot(edge.n) - edge.k
            if d > 0:
                return None
        return p

class Ellipsoid(object):
    __slots__ = ['c', 'v']

    def __init__(self, c, v):
        assert isinstance(c, euclid.Point3)
        assert isinstance(v, euclid.Vector3)
        self.c = c
        self.v = v

    def contact_ray(self, ray):
        # From http://www.gamedev.net/reference/articles/article1026.asp
        # I don't think this works.
        Q = ray.p - self.c
        c2 = Q.magnitude_squared()
        v = (Q * ray.v).magnitude_squared()
        d = 1. - (c2 - v * 2)
        if d < 0:
            return False
        return True

    def contact_ellipsoid(self, other):
        # This is not exact (why??), but close enough
        v = self.c - other.c
        vn = v.normalized()
        contact_r = abs(- self.v * vn) + abs(other.v * vn)
        return v.magnitude_squared() <  contact_r * contact_r

up = euclid.Vector3(0, 1, 0)

class Mesh(object):
    
    def __init__(self, meshes):
        # Naive
        self.polygons = []
        for mesh in meshes:
            self.polygons += mesh.polygons

        # Sparse uniform grid
        #print 'Building collision grid...'
        self.grid = {}
        interval = self.interval = 5
        for polygon in self.polygons:
            p1, p2 = polygon.aabbox
            x1 = int(round(p1.x / interval - 0.5))
            y1 = int(round(p1.y / interval - 0.5))
            z1 = int(round(p1.z / interval - 0.5))
            x2 = int(round(p2.x / interval - 0.5))
            y2 = int(round(p2.y / interval - 0.5))
            z2 = int(round(p2.z / interval - 0.5))
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    for z in range(z1, z2 + 1):
                        if (x, y, z) not in self.grid:
                            self.grid[x, y, z] = []
                        self.grid[x, y, z].append(polygon)
        #print '... %d cells' % len(self.grid.keys())
        #print '... %f polygons per cell' % \
        #    (sum([len(l) for l in self.grid.values()]) / \
        #        float(len(self.grid.values())))

    def get_polygons_within_aabox(self, p1, p2):
        x1 = int(round(p1.x / self.interval - 0.5))
        y1 = int(round(p1.y / self.interval - 0.5))
        z1 = int(round(p1.z / self.interval - 0.5))
        x2 = int(round(p2.x / self.interval - 0.5))
        y2 = int(round(p2.y / self.interval - 0.5))
        z2 = int(round(p2.z / self.interval - 0.5))
        polygons = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if (x, y, z) in self.grid:
                        polygons += self.grid[x, y, z]

        return set(polygons)
        
    def collide_ellipsoid(self, ellipsoid):
        # aabbox for ellipsoid
        p1 = ellipsoid.c - ellipsoid.v
        p2 = ellipsoid.c + ellipsoid.v

        result = []
        for poly in self.get_polygons_within_aabox(p1, p2):
            d = poly.contact_ellipsoid(ellipsoid)
            if d is not None:
                result.append((poly.plane, d))
        return result

    def collide_floor(self, segment):
        # aabox for line segment
        q1 = segment.p
        q2 = segment.p + segment.v
        p1 = euclid.Point3(min(q1.x, q2.x), min(q1.y, q2.y), min(q1.z, q2.z))
        p2 = euclid.Point3(max(q1.x, q2.x), max(q1.y, q2.y), max(q1.z, q2.z))

        best = None
        best_poly = None
        for poly in self.get_polygons_within_aabox(p1, p2):
            if poly.plane.n.dot(up) < 0.7: # 45 degree or less only
                continue
            p = poly.intersect_line3(segment)
            if p is not None:
                if best is None or p.y > best.y:
                    best = p
                    best_poly = poly
        return best, best_poly


from math import cos, sin

def offset(verts, dx, dy):
    newverts = []
    for i in range(0, len(verts), 2):
        newverts += [verts[i] + dx, verts[i+1] + dy]
    return newverts

def rotate(verts, angle):
    newverts = []
    angle = -angle # no idea
    for i in range(0, len(verts), 2):
        x, y = verts[i], verts[i+1]
        newverts += [
            x * cos(angle) - y * sin(angle),
            y * cos(angle) + x * sin(angle) ]
    return newverts


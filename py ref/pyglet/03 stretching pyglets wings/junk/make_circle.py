from math import cos, sin, pi

radius = 7
numSegs = 22

for i in range(numSegs+1):
    angle = 2*pi / numSegs * i
    x = sin(angle) * radius
    y = cos(angle) * radius
    print "    (%1.1f, %1.1f)," % (-y, x)


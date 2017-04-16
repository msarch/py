
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from PIL import Image
import aggdraw

img = Image.new("RGB", (2000, 2000), "white")
canvas = aggdraw.Draw(img)
brush = aggdraw.Brush("Red",00)
pen = aggdraw.Pen("black",0.5,200)

x0=160
y0=100
x1=100
y1=-400
x2=300
y2=160
x3=10
y3=100
n=5

p = aggdraw.Path()
p.moveto(0,0)
for i in range(n+1):
    t = i / n
    a = (1. - t)**3
    b = 3. * t * (1. - t)**2
    c = 3.0 * t**2 * (1.0 - t)
    d = t**3

    x = int(a * x0 + b * x1 + c * x2 + d * x3)
    y = int(a * y0 + b * y1 + c * y2 + d * y3)

    p.rlineto(x, y)
    #p.close()
    
canvas.path((10,10), p, pen,brush)
canvas.flush()


img.save("curve.png", "PNG")
img.show()



  
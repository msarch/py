

from PIL import Image
import aggdraw

img = Image.new("RGB", (2000, 2000), "white")
canvas = aggdraw.Draw(img)
brush = aggdraw.Brush("Red",00)
pen = aggdraw.Pen("black",3,200)

x0=1600
y0=100
x1=1000
y1=-4000
x2=3000
y2=1600
x3=100
y3=1000
n=50

pts = []
for i in range(n+1):
    t = i / n
    a = (1. - t)**3
    b = 3. * t * (1. - t)**2
    c = 3.0 * t**2 * (1.0 - t)
    d = t**3

    x = int(a * x0 + b * x1 + c * x2 + d * x3)
    y = int(a * y0 + b * y1 + c * y2 + d * y3)
    pts.append( (x, y) )
for i in range(n):
    canvas.line(((pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])),pen)


canvas.flush()
img.save("curve.png", "PNG")
img.show()

 
'''
The origin, 0,0; is the lower left, with x increasing to the right,
and Y increasing upwards.
 
The chardisplay above produces the following output :
+-----------------+
|                 |
|                 |
|                 |
|                 |
|         @@@@    |
|      @@@    @@@ |
|     @           |
|     @           |
|     @           |
|     @           |
|      @          |
|      @          |
|       @         |
|        @        |
|         @@@@    |
|             @@@@|
|                 |
+-----------------+
'''
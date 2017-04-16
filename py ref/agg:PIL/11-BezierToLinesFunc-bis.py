# Random Bezier Curve using De Casteljau's algorithm
# http://en.wikipedia.org/wiki/Bezier_curve
# http://en.wikipedia.org/wiki/De_Casteljau%27s_algorithm
# FB - 201111244
from PIL import Image, ImageDraw

def plot_curve(image, px, py, steps=1000, color=(0, 255, 0)):
    def B(coord, i, j, t):
        if j == 0:
            return coord[i]
        return (B(coord, i, j - 1, t) * (1 - t) +
                B(coord, i + 1, j - 1, t) * t)

    img = image.load()
    for k in range(steps):
        t = float(k) / (steps - 1)
        x = int(B(px, 0, n - 1, t))
        y = int(B(py, 0, n - 1, t))
        try:
            img[x, y] = color
        except IndexError:
            pass

def plot_control_points(image, px, py, radi=3, color=(255, 0, 0)):
    draw = ImageDraw.Draw(image)
    for x, y in zip(px, py):
        draw.ellipse((x - radi, y - radi, x + radi, y + radi), color)


# Your fixed, manually specified, points.
n = 4
coord_x = [25, 220, 430, 410]
coord_y = [250, 10, 450, 40]

image = Image.new("RGB", (500, 500))

plot_curve(image, coord_x, coord_y)
plot_control_points(image, coord_x, coord_y)

image.save("BezierCurve.png")
image.show()
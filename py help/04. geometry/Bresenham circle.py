from Tkinter import *

class BresenhamCanvas(Canvas):

    def draw_point(self, x, y, color="red"):
        self.create_line(x, y, x+1, y+1, fill=color)

    def draw_circle_points(self, x, y, center_x, center_y, color="red"):
        '''Draw 8 points on a circle centered
           at center_x, center_y, by symmetry.'''
        self.draw_point(center_x + x, center_y + y, color)
        self.draw_point(center_x - x, center_y - y, color)
        self.draw_point(center_x + x, center_y - y, color)
        self.draw_point(center_x - x, center_y + y, color)

        # If x == y then these points will simply duplicate
        # points already drawn above. No need to repeat them then.
        if x != y:
            self.draw_point(center_x + y, center_y + x, color)
            self.draw_point(center_x - y, center_y - x, color)
            self.draw_point(center_x + y, center_y - x, color)
            self.draw_point(center_x - y, center_y + x, color)

    def draw_circle(self, center_x, center_y, radius, line_thickness, color="red"):

        # Start at the top of the circle
        x = 0
        yin = radius - int(line_thickness/2)
        yout = radius + int(line_thickness/2)

        din = 1 - radius - int(line_thickness/2) # midpoint decision variable
        deltaEin = 3     # initial delta for move E
        deltaSEin = -2*(radius - int(line_thickness/2)) + 5 # initial delta for move SE
        dout = 1 - radius + int(line_thickness/2) # midpoint decision variable
        deltaEout = 3     # initial delta for move E
        deltaSEout = -2*(radius + int(line_thickness/2)) + 5 # initial delta for move SE

        # First point
        for y in range(yin,yout):
            self.draw_circle_points(x, y, center_x, center_y, color)

        # Stop when we cross the line y == x, which is the edge
        # of the first octant of the circle
        while yout > x:
            if din < 0:
                # Moving E
                din = din + deltaEin
                deltaEin = deltaEin + 2
                deltaSEin = deltaSEin + 2
            else:
                # Moving SE
                din = din + deltaSEin
                deltaEin = deltaEin + 2
                deltaSEin = deltaSEin + 4
                yin = yin - 1
            if dout < 0:
                # Moving E
                dout = dout + deltaEout
                deltaEout = deltaEout + 2
                deltaSEout = deltaSEout + 2
            else:
                # Moving SE
                dout = dout + deltaSEout
                deltaEout = deltaEout + 2
                deltaSEout = deltaSEout + 4
                yout = yout - 1
            x = x + 1
            for y in range(yin,yout):
                self.draw_circle_points(x, y, center_x, center_y, color)

def run():
    import math
    CANVAS_SIZE = 600

    root = Tk()
    canvas = BresenhamCanvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
    canvas.pack()

    margin = CANVAS_SIZE / 10

    origin_x = int(CANVAS_SIZE / 2)
    origin_y = int(CANVAS_SIZE / 2)
    center_dist = ((CANVAS_SIZE / 2) - 2*margin)
    radius = margin*2

    n_circles = 10
    angle_step = (2 * math.pi) / n_circles

    for i in range(n_circles):
        theta = angle_step * i
        center_x = int(center_dist * math.cos(theta)) + origin_x
        center_y = int(center_dist * math.sin(theta)) + origin_y
        canvas.draw_circle(center_x, center_y, radius, 10, color="blue")

    root.mainloop()


if __name__ == "__main__":
    run()

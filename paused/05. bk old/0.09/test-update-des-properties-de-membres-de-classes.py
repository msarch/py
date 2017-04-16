
class Vec2d:

    def __init__(self,x,y):
        self.vec= [x,y]
        self.half=(0.5*x, 0.5*y)

    def __repr__(self):
        return "Vec\t@(%.1d,%.1d)" % (self.vec[0],self.vec[1])

    def third(self):
           half=(0.3*self.vec[0], 0.3*self.vec[1])


a = Vec2d(10,20)
print a
b= a.half

a[0]=3.33
print a
b= a.half
print b

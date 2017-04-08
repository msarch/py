from vector import Vector, Spherical
import math

v1 = Vector([1,0,0])
v2 = Vector([0,1,0])

v3 = Spherical([1,90,90])




#         GENERAL FUNCTIONS
#--------------------------------------







def main():
    print v1
    print v2
    print v3
    w = Vector.dot(v1,v2)
    x = Vector.cross(v1,v2)
    print w
    print x



if __name__ == '__main__':
    main()



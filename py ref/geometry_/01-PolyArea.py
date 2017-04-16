# Function for finding the area of a polygon in a 2D co-ordinate system.
# {{{ http://code.activestate.com/recipes/578275/ (r1)
def poly_area2D(poly):
    total = 0.0
    N = len(poly)
    for i in range(N):
        v1 = poly[i]
        v2 = poly[(i+1) % N]
        total += v1[0]*v2[1] - v1[1]*v2[0]
    return abs(total/2)
# This function implements Green's theorem,
# also known as the shoelace theorem or the surveyors' theorem,
# which is the 2D case of the more general Stokes' theorem.
# http://www.mathpages.com/home/kmath201/kmath201.htm
# http://en.wikipedia.org/wiki/Shoelace_formula

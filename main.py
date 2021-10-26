from matplotlib.path import Path
from itertools import product
from numpy import polyfit
from random import randint

poly = [
    (0,0),
    (4,0),
    (1,1),
    (4,3),
    (0,3),
    (0,0),
]

poly = [ (randint(-7,12), randint(-7,12)) for i in range(randint(3, 10)) ]
poly += [poly[0]]
#poly = [
#    (0,0),
#    (4,0),
#    (1,1),
#    (4,3),
#    (0,3),
#    (0,0),
#]
#
poly = [
    (0,0),
    (0,5),
    (7,5),
    (5,2),
    (3,4),
    (1,2),
    (1,1),
    (3,3),
    (5,2),
    (7,4),
    (7,0),
    (0,0),
]
#poly = [
#    (0, 3),
#    (4, 5),
#    (4, 3),
#    (1, 0),
#    (0, 3),
#]

def point_in_poly(p, poly):
    x, y = p
    odd = False
    
    for segment_a, segment_b in zip(poly, poly[1:] + [poly[0]]):
        x_a, y_a = segment_a
        x_b, y_b = segment_b
        if (y_a < y <= y_b) or (y_b < y <= y_a):
            if (x_a + (y - y_a) / (y_b - y_a) * (x_b - x_a)) < x:
                odd = not odd
    
    return odd

def find_A_points(poly, B_points):
    
    min_x, max_x = min([x[0] for x in poly ]), max([x[0] for x in poly ])
    min_y, max_y = min([x[1] for x in poly ]), max([x[1] for x in poly ])
    all_points = set(product(range(min_x+1, max_x), range(min_y+1, max_y))) - B_points
    return set([point for point in all_points if point_in_poly(point, poly)])

def find_B_points(poly):
    def f(k, x ,b):
        return round(k * x + b,2)

    B_points = set(poly)

    for segment in [ poly[i:i+2] for i in range(len(poly)-1) ]:
        X = [x[0] for x in segment ]
        Y = [x[1] for x in segment ]
        min_x, max_x = min(X), max(X)
        try:
            assert min_x != max_x, 'vertical line'
            k, b = [ round(x,2) for x in polyfit(X, Y, 1) ]
            B_points |= set([ (x, f(k, x, b)) for x in range(min_x, max_x) if abs(f(k, x, b) - int(f(k, x, b))) < 0.01 ])
        except (ValueError, AssertionError):
            min_y, max_y = min(Y), max(Y)+1
            x = X[0]
            B_points |= set([ (x, y) for y in range(min_y, max_y) ])
            
    return B_points

B_points = find_B_points(poly)
A_points = find_A_points(poly, B_points)
A = len(A_points)
B = len(B_points)
S = A + B / 2 - 1

print("%s = %s + %s / 2 - 1" % (S, A, B))



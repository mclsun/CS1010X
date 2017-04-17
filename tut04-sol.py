############
# Question 1
############
def calc_integral(f, a, b, n):
    h = (b - a) /  n

    i, total = 0, 0
    while i <= n:
        term = f(a+i*h)
        if i == 0 or i == n:
            total += term
        elif i % 2 == 0:
            total += 2*term
        else:
            total += 4*term
        i += 1

    return (total * h) / 3.0

#print(calc_integral( lambda x : x*x*x, 0, 1, 10000))

############
# Question 2
############
def fold(op, f, n):
    if n == 0:
        return f(0)

    return op(f(n), fold(op, f, n-1))

def g(k):
    return fold(lambda x,y: x*y, lambda x: x - (x+1)*(x+1), k)

#print g(11)

############
# Question 3
############
def accumulate(combiner, base, term, a, next, b):
    if a > b:
        return base

    return combiner(term(a), accumulate(combiner, base, term, next(a), next, b))

def accumulate_iter(combiner, base, term, a, next, b):
    terms = ()

    # generate all the terms and put them in reverse order
    while a <= b :
        terms = (term(a),) + terms
        a = next(a)

    # combine the terms
    result = base
    for term in terms:
        result = combiner(term, result)

    return result

## two sample usages of accumulate, one for iteration and one for recursion
## verify that both acc_recur and acc_iter indeed produce the same output
acc_recur = accumulate(lambda x,y: x*y, 1, lambda x: x*x, 1, lambda x: x+1, 5)
acc_iter = accumulate_iter(lambda x,y: x*y, 1, lambda x: x*x, 1, lambda x: x+1, 5)
# print(acc_recur)
# print(acc_iter)

## define `sum` in terms of accumulate
def sum_acc(term, a, next, b):
    return accumulate(lambda x,y: x+y, 0, term, a, next, b)
def sum_acc_iter(term, a, next, b):
    return accumulate_iter(lambda x,y: x+y, 0, term, a, next, b)

## sum function as defined in lecture
def sum(term, a, next, b):
    if a > b:
        return 0

    return term(a) + sum(term, next(a), next, b)

#print(sum(lambda x: x*2, 1, lambda x: x+1, 5))

# Testing sum
def sum_iter(term, a, next, b):
    i, total = a, 0
    while i <= b:
        total += term(i)
        i = next(i)

    return total

#print (sum_iter(lambda x: x*2, 1, lambda x: x+1, 5))
#print (sum_acc(lambda x: x*2, 1, lambda x: x+1, 5))

#############
# Question 4a
#############
def print_point(p):
    print("(", x_point(p), ",", y_point(p), ")")

def make_point(x, y):
    def point(axis):
        if axis == 0:
            return x
        else:
            return y

    return point

def x_point(p):
    return p(0)

def y_point(p):
    return p(1)

# Alternative:
#
# def make_point(x,y):
#     return (x, y)
#
# def x_point(p):
#      return p[0]
#
# def y_point(p):
#      return p[1]

def make_segment(start_point, end_point):
    def segment(s):
        if s == 0:
            return start_point
        else:
            return end_point
    return segment

def start_segment(segment):
    return segment(0)
def end_segment(segment):
    return segment(1)

def midpoint_segment(segment):
    start_point = start_segment(segment)
    end_point = end_segment(segment)

    mid_x = 0.5 * (x_point(start_point) + x_point(end_point))
    mid_y = 0.5 * (y_point(start_point) + y_point(end_point))

    return make_point(mid_x, mid_y)

## sample usage of midpoint_segment
p0 = make_point(0,0)
p1 = make_point(4,4)
segment = make_segment(p0, p1)
p_mid = midpoint_segment(segment)

#############
# Question 4b
#############

## first representation of a Rectangle, together with selectors
def rect_a(length_segment, width_segment):
    def segment(s):
        if s == 0:
            return length_segment
        else:
            return width_segment
    return segment

def rect_length_segment(rect_a):
    return rect_a(0)
def rect_width_segment(rect_a):
    return rect_a(1)

## selector for a length of a Segment
import math
def segment_length(segment):
    start_point = start_segment(segment)
    end_point = end_segment(segment)

    x_delta = x_point(start_point) - x_point(end_point)
    y_delta = y_point(start_point) - y_point(end_point)

    return math.sqrt(x_delta*x_delta + y_delta*y_delta)

## sample usage of segment_length
length = segment_length(make_segment(make_point(0,0), make_point(2,2)))
print(length)

def rect_length(rect):
    return segment_length(rect_length_segment(rect))
def rect_width(rect):
    return segment_length(rect_width_segment(rect))

def perimeter(rect):
    return 2*rect_length(rect) + 2*rect_width(rect)

def area(rect):
    return rect_length(rect) * rect_width(rect)

## alternative representation of a Rectangle
# Give 3 consective clockwise points of the rectangle
def rect_b(p0, p1, p2):
    def point(p):
        if p == 0:
            return p0
        elif p == 1:
            return p1
        else:
            return p2
    return point

# We need to implement the length_segment and width_segment for rect b
def rect_length_segment(rect_b):
    return make_segment(rect_b(0), rect_b(1))
def rect_width_segment(rect_b):
    return make_segment(rect_b(1), rect_b(2))

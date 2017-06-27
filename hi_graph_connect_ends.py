from tkinter import *
from math import sin, cos, pi, sqrt, atan2
import time
import atexit, sys, threading

## Increase rursion stack size
sys.setrecursionlimit(2**20)

## Configuration
WINDOW_SIZE = 512
BORDER_OFFSET = 8

## Some dervived values
CANVAS_SIZE = {'x': BORDER_OFFSET, 
                'y': BORDER_OFFSET, 
                'width': WINDOW_SIZE-2*BORDER_OFFSET, 
                'height': WINDOW_SIZE-2*BORDER_OFFSET}

## Some helper functions
def identity(x):
    return x

def composed(f, g):
    return lambda x: f(g(x))

def repeated(f, n):
    if (n == 0):
        return identity
    return composed(f, repeated(f, n-1))

## Data abstraction
def make_point(x,y):
    return lambda p: x if p == 0 else y

def x_of(point):
    return point(0)

def y_of(point):
    return point(1)

def tupify_point(point):
    return (x_of(point), y_of(point))

## Curve Functions
def unit_circle(t):
    return make_point(sin(2*pi*t), cos(2*pi*t))

def alternative_unit_circle(t):
    return make_point(sin(2*pi*t*t), cos(2*pi*t*t))

def unit_line_at_y(y):
    return lambda t: make_point(t, y)

unit_line = unit_line_at_y(0)

def arc(t):
    return make_point(sin(pi*t), cos(pi*t))

## Curve Transformation Function
def rotate_90(curve):
    def rotated_curve(t):
        pt = curve(t)
        return make_point(-y_of(pt), x_of(pt))
    return rotated_curve

def revert(curve):
    return lambda t: curve(1-t)

## Constructors of Curve Transforms
def rotate(angle):
    def transform(curve):
        def rotated_curve(t):
            pt = curve(t)
            x, y = x_of(pt), y_of(pt)
            cos_a, sin_a = cos(angle), sin(angle)

            return make_point(cos_a*x - sin_a*y, sin_a*x + cos_a*y)
        return rotated_curve
    return transform

def joe_rotate(angle):
    def transform(curve):
        def rotated_curve(t):
            x, y = x_of(curve(t)), y_of(curve(t))
            cos_a, sin_a = cos(angle), sin(angle)

            return make_point(cos_a*x - sin_a*y, sin_a*x + cos_a*y)
        return rotated_curve
    return transform

def translate(x,y):
    def transform(curve):
        def translated_curve(t):
            pt = curve(t)
            return make_point(x_of(pt)+x, y_of(pt)+y)
        return translated_curve
    return transform

def scale_xy(s_x,s_y):
    def transform(curve):
        def scaled_curve(t):
            pt = curve(t)
            return make_point(s_x*x_of(pt), s_y*y_of(pt))
        return scaled_curve
    return transform

def scale(s):
    return scale_xy(s,s)

## Binary Transforms
def connect_rigidly(curve1, curve2):
    def connected_curve(t):
        if (t < 0.5):
            return curve1(2*t)
        else:
            return curve2(2*t - 1)
    return connected_curve

def connect_ends(curve1, curve2):
    curve2_start = curve2(0)
    curve1_end = curve1(1)

    x_delta = x_of(curve1_end) - x_of(curve2_start)
    y_delta = y_of(curve1_end) - y_of(curve2_start)

    new_curve2 = translate(x_delta, y_delta)(curve2)
    return connect_rigidly(curve1, new_curve2)

## TK Setup code
root = None
num_windows = 0
atexit.register(lambda: root.mainloop() if root else None)

## TK Helper Functions
def get_window():
    def delete_handler():
        global root, num_windows
        root.destroy()
        root = None
        num_windows = 0

    global root, num_windows
    num_windows += 1
    if root:
        return Toplevel()
    else:
        root = Tk()
        root.protocol("WM_DELETE_WINDOW", delete_handler)
        return root

def get_canvas(title):
    w = get_window()
    w.wm_title("W{} : {}".format(num_windows, title))

    c = Canvas(w, width=WINDOW_SIZE, height=WINDOW_SIZE, relief='groove')
    c.master.maxsize(WINDOW_SIZE,WINDOW_SIZE)
    c.master.minsize(WINDOW_SIZE,WINDOW_SIZE)
    c.pack()
    return c

def canvas_coord(p):
    x,y = p[0], p[1]
    return (CANVAS_SIZE['x'] + x*CANVAS_SIZE['width'],
            CANVAS_SIZE['y'] + (1-y)*CANVAS_SIZE['height'])

def points_for_curve(n, curve):
    return [tupify_point(curve(i/n)) for i in range(0, n+1)]

def scaled_points_for_curve(n, curve):
    points = points_for_curve(n, curve)
    x_ofs = list(map(lambda p: p[0], points))
    y_ofs = list(map(lambda p: p[1], points))

    min_x = min(x_ofs)
    max_x = max(x_ofs)
    min_y = min(y_ofs)
    max_y = max(y_ofs)
    delta_x = max(0.00001, max_x - min_x)
    delta_y = max(0.00001, max_y - min_y)

    return list(map(lambda p: ((p[0] - min_x) / delta_x, (p[1] - min_y) / delta_y), points))

## Drawing Functions
def draw_connected(n, curve):
    points = points_for_curve(n, curve)

    c = get_canvas("draw_connected({},{})".format(n, curve.__name__))
    for i in range(0, n):
        src, dest = canvas_coord(points[i]), canvas_coord(points[i+1])
        c.create_line(*(src+dest))

def draw_connected_scaled(n, curve):
    points = scaled_points_for_curve(n, curve)
    c = get_canvas("draw_connected_scaled({}, {})".format(n, curve.__name__))
    for i in range(0, n):
        src, dest = canvas_coord(points[i]), canvas_coord(points[i+1])
        c.create_line(*(src+dest))

def draw_points(n, curve):
    points = points_for_curve(n, curve)

    c = get_canvas("draw_points({},{})".format(n, curve.__name__))
    for p in points:
        c.create_text(*(canvas_coord(p)), text=".")

def draw_points_scaled(n, curve):
    points = scaled_points_for_curve(n, curve)

    c = get_canvas("draw_points_scaled({},{})".format(n, curve.__name__))
    for p in points:
        c.create_text(*(canvas_coord(p)), text=".")

def squeeze_curve_to_rect(x_low, y_low, x_high, y_high):
    width = x_high - x_low
    height = y_high - y_low

    return composed(scale_xy(1/width, 1/height), translate(-x_low, -y_low))

def put_in_standard_position(curve):
    start_point = curve(0)
    curve_at_origin = translate(-x_of(start_point),-y_of(start_point))(curve)

    new_end_point = curve_at_origin(1)
    theta = atan2(y_of(new_end_point), x_of(new_end_point))
    curve_ended_at_x = rotate(-theta)(curve_at_origin)
    end_point_on_x = x_of(curve_ended_at_x(1))

    return scale(1/end_point_on_x)(curve_ended_at_x)

## Fractals

def gosperize(curve):
    scaled_curve = scale(sqrt(2)/2)(curve)
    left_curve = rotate(pi/4)(scaled_curve)
    right_curve = translate(0.5,0.5)(rotate(-pi/4)(scaled_curve))

    return connect_rigidly(left_curve, right_curve)

def gosper_curve(level):
    return repeated(gosperize, level)(unit_line)

def show_connected_gosper(level):
    squeezed_curve = squeeze_curve_to_rect(-0.5, -0.5, 1.5, 1.5)(gosper_curve(level))
    draw_connected(200, squeezed_curve)

def gosperize_with_angle(theta):
    def inner_gosperize(curve):
        scale_factor = (1 / cos(theta)) / 2
        scaled_curve = scale(scale_factor)(curve)
        left_curve = rotate(theta)(scaled_curve)
        right_curve = translate(0.5,sin(theta)*scale_factor)(rotate(-theta)(scaled_curve))
        return connect_rigidly(left_curve, right_curve)
    return inner_gosperize

def gosper_curve_with_angle(level, angle_at_level):
    if level == 0:
        return unit_line
    else:
        angle = angle_at_level(level)
        return gosperize_with_angle(angle)(gosper_curve_with_angle(level-1, angle_at_level))
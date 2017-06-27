#
# CS1010X --- Programming Methodology
#
# Mission 5
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from hi_graph import *

##########
# Task 1 #
##########
def connect_rigidly ( curve1 , curve2 ):
    def connected_curve ( t ):
        if ( t < 0.5 ):
            return curve1 ( 2 * t )
        else :
            return curve2 ( 2 * t - 1 )
    return connected_curve

def connect_ends(curve1, curve2):
    end_1 = curve1(1)
    start_2 = curve2(0)
    
    end_1_x = x_of(end_1)
    end_1_y = y_of(end_1)
    
    start_2_x = x_of(start_2)
    start_2_y = y_of(start_2)
    
    offset_x = end_1_x - start_2_x
    offset_y = end_1_y - start_2_y
    
    return connect_rigidly(curve1, translate(offset_x, offset_y)(curve2))
# draw_connected_scaled(200, connect_ends(arc, unit_line))
# draw_connected_scaled(200, connect_ends(translate(5,5)(arc), translate(1,1)(unit_line)))

##########
# Task 2 #
##########

def show_points_gosper(level, num_points, initial_curve):
    def gosper_curve (level, initial_curve):
        return repeated(gosperize, level)(initial_curve)
    squeezed_curve = squeeze_curve_to_rect (-0.5, -0.5, 1.5, 1.5)(gosper_curve(level, initial_curve))
    return draw_points(num_points, squeezed_curve)
# show_points_gosper(7, 1000, arc)

##########
# Task 3 #
##########

def your_gosper_curve_with_angle(level, angle_at_level):
    if level == 0:
        return unit_line
    else:
        return your_gosperize_with_angle(angle_at_level(level))(your_gosper_curve_with_angle(level-1, angle_at_level))

# left curve, right curve
# rotate ( theta )( arg_curve )

def your_gosperize_with_angle(theta):
    def inner_gosperize(curve_fn):
        return put_in_standard_position(connect_ends(rotate(theta)(curve_fn), rotate(-theta)(curve_fn)))
    return inner_gosperize

# testing
# draw_connected(200, your_gosper_curve_with_angle(10, lambda lvl: pi/(2+lvl)))
draw_connected(200, your_gosper_curve_with_angle(5, lambda lvl: (pi/(2+lvl))/(pow(1.3, lvl))))

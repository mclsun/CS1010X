#
# CS1010X --- Programming Methodology
#
# Mission 6
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from diagnostic import *
from hi_graph_connect_ends import *

# Mission 6 requires certain functions from Mission 5 to work.
# Do copy any relevant functions that you require in the space below:
    
def your_gosper_curve_with_angle(level, angle_at_level):
    if level == 0:
        return unit_line
    else:
        return your_gosperize_with_angle(angle_at_level(level))(your_gosper_curve_with_angle(level-1, angle_at_level))

def your_gosperize_with_angle(theta):
    def inner_gosperize(curve_fn):
        return put_in_standard_position(connect_ends(rotate(theta)(curve_fn), rotate(-theta)(curve_fn)))
    return inner_gosperize

# Do not copy any other functions beyond this line #
##########
# Task 1 #
##########

# Example from the mission description on the usage of time function:
# profile_fn(lambda: gosper_curve(1000)(0.1), 500)

# Choose a significant level for testing for all three sets of functions.

def average_of_five(function):
    sum = 0
    for i in range(0, 5):
        a = function
        print(a)
        sum += a
    return sum / 5

# -------------
# gosper_curve:
# -------------
# write down and invoke the function that you are using for this testing
# in the space below

print(profile_fn ( lambda : gosper_curve(10)(0.1), 10))

print('average: ' + str(average_of_five(profile_fn ( lambda : gosper_curve(10)(0.1), 10))))


# ------------------------
# gosper_curve_with_angle:
# ------------------------
# write down and invoke the function that you are using for this testing
# in the space below

print(profile_fn ( lambda : gosper_curve_with_angle(10, lambda lvl : pi/4)(0.1), 10))

print('average: ' + str(average_of_five(profile_fn ( lambda : gosper_curve_with_angle(10, lambda lvl : pi/4)(0.1), 10))))

#
# -----------------------------
# your_gosper_curve_with_angle:
# -----------------------------
# write down and invoke the function that you are using for this testing
# in the space below

print(profile_fn ( lambda : your_gosper_curve_with_angle(10, lambda lvl : pi/4)(0.1), 10))

print('average: ' + str(average_of_five(profile_fn ( lambda : your_gosper_curve_with_angle(10, lambda lvl : pi/4)(0.1), 10))))


# Conclusion:
# (Times below are to 2 decimal places)
# There is no speed advantage for the more customized functions where angle is fixed.
# Because gosper_curve which is customized takes around the same time as gosper_curve_with_angle (1.58s and 1.99s respectively).
# In addition, both gosper_cuve_with_angle and your_gosper_curve_with_angle are customisable but differ largly in their times (1.99s and 18.26s respectively)
# Hence, customization is not the main factor affecting time.


##########
# Task 2 #
##########

#  1) Yes, because curve(t) evaluates to pt so their outputs are the same.


#  2) joe_rotate evaluates curve(t) each time it is called (twice in joe_rotate) wheras rotate evaluates it once,
#     stores it in the variable pt and uses the stored value when pt is called.
#     Via repeated, gosper_curve calls gosperize recursively, gosperize calls rotate twice.
#     This is similar to traversing a binary tree where complexity is exponential as level increases.
#     Therefore, time complexity for joe_rotate becomes exponential instead of linear 

##########
# Task 3 #
##########



#
# Fill in this table:
#
#                    level      rotate       joe_rotate
#                      1           3            4
#                      2           5            10
#                      3           7            22
#                      4           9            46
#                      5          11            94
#
#  Evidence of exponential growth in joe_rotate.


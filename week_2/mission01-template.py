#
# CS1010X --- Programming Methodology
#
# Mission 1
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from runes import *


##########
# Task 1 #
##########

def mosaic(a, b, c, d):
    clear_all()
    return beside(stack(d, c), stack(a, b))


# Test
#show(mosaic(rcross_bb, sail_bb, corner_bb, nova_bb))

##########
# Task 2 #
##########

def simple_fractal(pic):
    clear_all()
    return beside(pic, stack(pic, pic))

# Test
show(simple_fractal(make_cross(rcross_bb)))



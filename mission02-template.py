#
# CS1010X --- Programming Methodology
#
# Mission 2
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from runes import *


###########
# Task 1a #
###########

def fractal(pic, n):
    if n == 1:
        return pic
    return beside(pic, stackn(2, fractal(pic, n-1)))

# 2: beside(pic, stackn(2, pic))
# 3: beside(pic, stackn(2, beside(pic, stackn(2, pic))))                 

# Test
# show(fractal(make_cross(rcross_bb), 3))
# show(fractal(make_cross(rcross_bb), 7))
# Write your additional test cases here

###########
# Task 1b #
###########

def fractal_iter(pic, n):
    i, picture = 1, pic
    while i < n:
        picture = beside(pic, stackn(2, picture))
        i += 1
    return picture
                         
# Test
# show(fractal_iter(make_cross(rcross_bb), 3))
# show(fractal_iter(make_cross(rcross_bb), 7))
# Write your additional test cases here


###########
# Task 1c #
###########
def dual_fractal(pic1, pic2, n):
    if n == 1:
        return pic1
    return beside(pic1, stackn(2, dual_fractal(pic2, pic1, n-1)))
                         
# Test
# show(dual_fractal(make_cross(rcross_bb), make_cross(nova_bb), 3))
# show(dual_fractal(make_cross(rcross_bb), make_cross(nova_bb), 4))
# show(dual_fractal(make_cross(rcross_bb), make_cross(nova_bb), 7))
# Write your additional test cases here

# Note that when n is even, the first (biggest) rune should still be rune1

###########
# Task 1d #
###########
def dual_fractal_iter(pic1, pic2, n):
    # if n is even, rightmost should be pic2.
    if n % 2 == 1:
        right = pic
    else:
        right = pic2
      
    for i in range(n, 1, -1):
        pic1, pic2 = pic2, pic1
        right = beside(pic2, stack(right, right))
    return right

# Test
show(dual_fractal_iter(make_cross(rcross_bb), make_cross(nova_bb), 3))
# show(dual_fractal_iter(make_cross(rcross_bb), make_cross(nova_bb), 4))
# show(dual_fractal_iter(make_cross(rcross_bb), make_cross(nova_bb), 7))
# Write your additional test cases here

# Note that when n is even, the first (biggest) rune should still be rune1

##########
# Task 2 #
##########

def steps(A, B, C, D):
    a_quarter = beside(blank_bb, stack(A, blank_bb))
    b_quarter = beside(blank_bb, stack(blank_bb, B))
    c_quarter = beside(stack(blank_bb, C), blank_bb)
    d_quarter = beside(stack(D, blank_bb), blank_bb)
    return overlay(overlay(d_quarter, c_quarter), overlay(b_quarter, a_quarter))

# Test
# show(steps(rcross_bb, sail_bb, corner_bb, nova_bb))

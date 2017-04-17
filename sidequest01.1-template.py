#
# CS1010X --- Programming Methodology
#
# Mission 1 - Side Quest
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from runes import *

##########
# Task 1 #
##########

def egyptian(pic, n):
    hori_center = build_hori_center(pic, n)
    row = make_row(pic, n)
    needs_rotation = sandwich(row, hori_center, n)
    return quarter_turn_left(needs_rotation)

def build_hori_center(pic, n):
    row = quarter_turn_left(make_column(pic, n))
    center = quarter_turn_left(pic)
    return sandwich(row, center, n)

def sandwich(row, pic, n):
    mash_temp = stack_frac(1/(n-1), row, pic)
    needs_rotation = stack_frac(1/n, turn_upside_down(row), turn_upside_down(mash_temp))
    return quarter_turn_left(needs_rotation)
    
def make_column(pic, n):
    return stackn(n-2, pic)

def make_row(pic, n):
    return quarter_turn_right(stackn(n, quarter_turn_left(pic)))
    
# Test
#show(egyptian(make_cross(rcross_bb), 5))

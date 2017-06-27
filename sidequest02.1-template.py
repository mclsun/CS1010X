#
# CS1010X --- Programming Methodology
#
# Mission 2 - Side Quest 1
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

from runes import *
import math

##########
# Task 1 #
##########

def tree(n, pic):
    result = pic
    for i in range(2, n+1):
        result = overlay_frac(1/i, scale((n-i+1)/n, pic), result)
    return result

# Test
# show(tree(4, circle_bb))


##########
# Task 2 #
##########

# use help(math) to see functions in math module
# e.g to find out value of sin(pi/2), call math.sin(math.pi/2)

def helix(pic, n):
    R = 1/2 - 1/n
    A = 2 * math.pi/n
    def small_pic(i):
        return translate(R * math.cos(math.pi/2 + i * A),
                         R * math.sin(math.pi/2 + i * A),
                         scale(2/n, pic))
    result = small_pic(1)
    for i in range(2, n+1):
        result = overlay_frac(1/i, small_pic(i), result)
    return result
    
    

# Test
show(helix(make_cross(rcross_bb), 12))

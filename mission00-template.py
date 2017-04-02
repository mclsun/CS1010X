#
# CS1010X --- Programming Methodology
#
# Mission 0
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.

# The expected answer is what you think the line of code will produce if it were to be run in IDLE.
# The final answer is the output after running the line of code in IDLE.

# The first line has already been uncommented for you. Just press F5 to run this file in IDLE

##########
# Task 1 #
##########

print(42)
# expected answer: 42
# final answer:

print(0000)
# expected answer: 0
# final answer:

print("the force!")
# expected answer: "the force!"
# final answer:

print("Hello World")
# expected answer: "Hello World"
# final answer:

# print "Hello World"
# expected answer error
# final answer:

print(6 * 9)
# expected answer: 54
# final answer:

print(2 + 3)
# expected answer: 5
# final answer:

print(2 ** 4)
# expected answer: 16
# final answer:

print(2.1**2.0)
# expected answer: 4.41
# final answer:

print(15 > 9.7)
# expected answer: True
# final answer:

print((5 + 3) ** (5 - 3))
# expected answer: 64
# final answer:

print(--4)
# expected answer: 4
# final answer:

print(1 / 2)
# expected answer: 0.5
# final answer:

print(1 / 3)
# expected answer: 0.3333333333333333
# final answer:

# print(1 / 0)
# expected answer: error
# final answer:

print(7 / 3 == 7 / 3.0)
# expected answer: True
# final answer:

print(3 * 6 == 6.0 * 3.0)
# expected answer: True
# final answer:

print(11 % 3)
# expected answer: 2
# final answer:

print(2 > 5 or (1 < 2 and 9 >= 11))
# expected answer: False
# final answer:

print(3 > 4 or (2 < 3 and 9 > 10))
# expected answer: False
# final answer:

print("2" + "3")
# expected answer: "23"
# final answer:

print("2" + "3" == "5")
# expected answer: False
# final answer:

print("2" <= "5")
# expected answer: True
# final answer:

print("2 + 3")
# expected answer: "2 + 3"
# final answer:

print("May the force" + " be " + "with you")
# expected answer: "May the force be with you"
# final answer:

print("force"*3)
# expected answer: "forceforceforce"
# final answer:

print('daw' in 'padawan')
# expected answer: True
# final answer:

a, b = 3, 4 # Do not comment this line

print(a)
# expected answer: 3
# final answer:

print(b)
# expected answer: 4
# final answer:

a, b = b, a # Do not comment this line

print(a)
# expected answer: 4
# final answer:

print(b)
# expected answer: 3
# final answer:

# print(red == 44)
# expected answer: error
# final answer:

red, green = 44, 43 # Do not comment this line

print(red == 44)
# expected answer: True
# final answer:

# print(red = 44)
# expected answer: error
# final answer:

print("red is 1") if red == 1 else print("red is not 1")
# expected answer: "red is not 1"
# final answer:

print(red - green)
# expected answer: 1
# final answer:

purple = red + green # Do not comment this line

print("purple")
# expected answer: "purple"
# final answer:

print(red + green != purple + purple / purple - red % green)
# expected answer: True
# final answer: False

print(green > red)
# expected answer: False
# final answer:

print("green bigger") if green > red else print("red equal or bigger")
# expected answer: "red equal or bigger"
# final answer:

print(green + 5)
# expected answer: 48
# final answer:

print(round(1.8))
# expected answer: 2
# final answer:

print(int(1.8))
# expected answer: 1
# final answer:

# The following question is to ensure that you have installed
# PILLOW, matplotlib, scipy, and numpy correctly.
# Do not worry about the syntax - just uncomment the line and observe
# the output (if any)

from PIL import *
# expected answer:
# final answer:

from matplotlib import *
# expected answer:
# final answer:

from scipy import *
# expected answer:
# final answer:

from numpy import *
# expected answer:
# final answer:

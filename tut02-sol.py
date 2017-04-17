from math import *

## Qn 1
# Import math package
from math import *

def magnitude(x1, y1, x2, y2):
    # Returns the magnitude of the vector
    # between (x1, y1) and (x2, y2).
    hori_square = square(x1-x2)
    vert_square = square(y1-y2)
    return sqrt(hori_square + vert_square)

def square(n):
    return n ** 2

### Answers:
# def magnitude(x1, y1, x2, y2):
#    return sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

## Qn 2(a)
def area(base, height):
    return 0.5 * base * height

## Qn 2(b)
def area2(A, B, included_angle):
    return 0.5 * A * B * sin(included_angle)

## Qn 2(c)
# No, they cannot. The arguments for the two functions are different.

## Qn 2(d)
def area3(ax, ay, bx, by, cx, cy):
    a = magnitude (ax, ay, bx, by)
    b = magnitude (bx, by, cx, cy)
    c = magnitude (cx, cy, ax, ay)
    return herons_formula(a, b, c)

def herons_formula(a, b, c):
    s = (a + b + c) / 2
    return sqrt(s * (s - a) * (s - b) * (s - c))

## Qn 3(a) What is the value of i at the end of the loop?
def foo1():
    i = 0
    result = 0
    while i < 10:
        result += i
        i += 1
    return result

# result: 45, i: 10

## Qn 3(b)
def foo2():
    i = 0
    result = 0
    while i < 10:
        if i == 3:
            break
        result += i
        i += 1
    return result

# result: 3, i: 3

## Qn 3(c)
def bar1():
    result = 0
    for i in range(10):
        result += i
    return result

# result: 45, i: 9

## Qn 3(d)
def bar2():
    result = 0
    for i in range(10):
        if i % 3 == 1:
            continue
        result += i
    return result

# result: 33, i: 9

## Qn 4
def sum_even_factorials(n):
    # Returns the sum of factorials of even numbers 
    # that are less than or equal to n.
    if n == 0:
        return 1
    if n % 2 == 1: # if odd
        return factorial(n-1) + sum_even_factorials(n-3)
    else:
        return factorial(n) + sum_even_factorials(n-2)

def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)
    
''' ANSWERS
def sum_even_factorials(n):
    result = 0
    for i in range(0, n+1):
        f = 1
        if i % 2 != 0:
            continue
        else:
            for j in range(1, i+1):
                f *= j
        result += f
    return result

def sum_even_factorials(n):
    result = 1 #Assuming n>=0
    factorial = 1
    for i in range(1,n+1):
        factorial *= i #calculate the factorial of i
        if i % 2 == 0: #if the i is even, we add the factorial
            result += factorial
    return result
'''

# print("Sum of even factorials: ", sum_even_factorials(0))
# print("Sum of even factorials: ", sum_even_factorials(3))
# print("Sum of even factorials: ", sum_even_factorials(6))

## Qn 5
def f(g):
    return g(2)

def square(x):
    return x ** 2

# print(f(square))
# print(f(lambda z: z * (z + 1)))

# Ans: It will give "TypeError: 'int' object is not callable".
# Passing f into the function f will cause the statement `return f(2)` to
# be evaluated. When 2 is passed into f as an argument, it tries to return 2(2).
# 2 is an integer, and not a function and cannot be invoked/called. 
# Hence TypeError occurs.

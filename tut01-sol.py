#####  Question 1

def square(x):
    return x ** 2

# print(square(2))
print_square_2 = 4 # An example answer

# print(square(4))
print_square_4 = 16 # Insert your answer here


# print(square(square(square(2))))
print_square_square_square_2 = 256 # Insert your answer here


def f(x):
    return x * x

# print(f(4))
print_f_4 = 16 # Insert your answer here


def try_f(f):
    return f(3)

# print(try_f(f))
print_try_f_f = 9 # Insert your answer here

# print(try_f(f) == try_f(square))
print_try_try = True # Insert your answer here

# print(f(3) == square(3))
print_f_3_equals_square_3 = True # Insert your answer here

# print(f == square)
print_f_equals_square = False # Insert your answer here

#####  Question 2

def odd(x):
    if x % 2 == 1:
        return True
    else:
        return False

#####  Question 3

def new_odd(x):
    return x % 2 == 1


#####  Question 4
# OOh recursion
def number_of_digits(i):
    if abs(i) < 10:
        return 1
    else:
        return 1 + number_of_digits(i // 10)

## Same as my answer:
def number_of_digits(i):
    return len(str(i))

# Question: Which solution is 'better'?
#           What if the question is now how do you get the sum of
#           all the digits of an integer?
#           What is wrong with the if, elif, elif, elif, ... approach?

#####  Question 5

def square(x):
    return x ** 2

def sum_of_squares(x, y):
    return square(x) + square(y)

def bigger_sum(a, b, c):
    if a <= b and a <= c: # alternatively, b >= a <= c
        return sum_of_squares(b, c)
    elif b <= a and b <= c: # alternatively, a >= b <= c
        return sum_of_squares(a, c)
    else:
        return sum_of_squares(a, b)

#####  Question 6

def is_leap_year(year):
    if year % 400 == 0:
        return True
    elif year % 4 == 0 and year % 100 != 0:
        return True
    else:
        return False

# Answer
def is_leap_year(year):
    return (year % 400 == 0) or (year % 4 == 0 and not year % 100 == 0)

# Possibly a more direct translation of the Wikipedia definition:
# (year % 4 == 0) and not (year % 100 == 0 and not year % 400 == 0)

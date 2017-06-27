### QN 1
def deep_reverse(lst):
    if type(lst) != list:
        return lst
    if len(lst) == 0:
        return []
    else:
        return deep_reverse(lst[1:]) + [deep_reverse(lst[0]),]
#print(deep_reverse([1, 2,[3, 4], [[5]], [6, [7, 8], 9]]))


### QN 2
def deep_sum(lst):
    if type(lst) != list:
        return lst
    if len(lst) == 0:
        return 0
    else:
        return deep_sum(lst[1:]) + deep_sum(lst[0])
#print(deep_sum([1, 2, [3, 4, [[5]], [[6], [7, 8], 9], 10]]))


### QN 3
def bubble_sort(lst):
    pass


# QN 4A:
def make_stack():
    stack = []
    def dispatch(msg, *args):
        if msg == 'push':
             stack.extend(args)
        elif msg == 'peek':
            if not stack:
                return None
            else:
                return stack[-1]
        elif msg == 'pop':
            if not stack:
                return None
            else:
                return stack.pop()
        elif msg == 'size':
            return len(stack)
        else:
            raise Error
    return dispatch

stk = make_stack()
stk('push',1)
stk('push',2)
stk('push',3)
print(stk('peek'))
#3
print(stk('pop'))
#3
print(stk('peek'))
#2
print(stk('size'))
#2


### QN 4B

## Method 1: push from first elems
## pseudocode

## eg + + *54 -21 3
## only works if operators are binary (2 inputs)
## push all elems into a stack
## if 2 numbers at top of stack, pop last 3 and evaluate (2*4) and push back into stack
def prefix_infix(lst):
    pass
        
## Method 2: reverse
def prefix_infix(sequ):
    stack = []
    seq = sequ.copy()
    seq.reverse()
    for c in seq:
        if type(c) == int:
            stack.append(c)
        else:
            l = stack.pop()
            r = stack.pop()
            exp = "f{l}{c}{r}"
            stack.append(exp)
    return stack[-1]

### QN 5
def enumerate_interval(min, max):
    return list(range(min, max+1))

def map(fn, seq):
    if seq == []:
        return ()
    else:
        return (fn(seq[0]), ) + map(fn, seq[1:])
def filter(pred, seq):
    if seq == []:
        return ()
    elif pred(seq[0]):
        return (seq[0],) + filter(pred, seq[1:])
    else:
        return filter(pred, seq[1:])
def accumulate(fn, initial, seq):
    if seq == []:
        return initial
    else:
        return fn(seq[0], accumulate(fn, initial, seq[1:]))

print(enumerate_interval(1,8))

print(list(map(lambda x: x*5, enumerate_interval(1, 12))))
print([x * 5 for x in enumerate_interval(1, 12)])

print(list(map(lambda x: x**2, list(filter(lambda x: x % 2 == 1,enumerate_interval(1, 12))))))
print([x**2 for x in enumerate_interval(1, 12) if x % 2 == 1])

print(list(map(lambda x: x**2 if x % 2 == 1 else x//2, enumerate_interval(1, 10))))
print([x**2 if x % 2 == 1 else x//2 for x in enumerate_interval(1, 10)])

print(list(map(lambda x: x**2 if x % 2 == 1 else x//2, enumerate_interval(1, 10))))
print([x**2 if x % 2 == 1 else x//2 for x in enumerate_interval(1, 10)])


## QN 6:
'''
power set of {}        = {}
power set of {1}       = {1} + previous
power set of {1, 2}    = {2}, {1, 2} + previous
power set of {1, 2, 3} = {3}, {1, 3}, {2, 3}, {1, 2, 3} + all previous
'''
def power_set(seq):
    if seq == []:
        return [[]]
    else:
        p = power_set(seq[1:])
        for elem in p.copy():
            p.append(e + [seq[0]])
        return p

# generate powerset of the longest elem
# check that its the same (have to deep sort)
def power_set_check(lst):
    power_set_longest = power_set(longest_elem(lst))
    

def longest_elem(lst):
    longest = lst[0]
    for i in lst:
        if len(i) > len(longest):
            longest = i
    return longest

def deep_sort(lst):
    ##if len(lst) == 0:
        ##return []
    ##if not lst
    pass

## QN 7:
class Number(object):
    def __init__(self, val):
        self.val = val
        
    def value(self):
        return self.val
    
    def minus(self, number):
        if self.val == 'Undefined' or number.val == 'Undefined':
             return Number('Undefined')
        else:
            return Number(self.val - number.val)
    
    def times(self, number):
        return Number(self.val * number.val)
    
    def divide(self, number):
        if number.val == 0:
            return Undefined()
        else:
            return Number(self.value() / number.value())
        
    def plus(self, number):
        if self.val == 'Undefined' or number.val == 'Undefined':
             return Number('Undefined')
        else:
            return Number(self.value() + number.value())
        
class Undefined(Number):
    def __init__(self):
        super().__init__("Undefined")
    def add(self, n):
        return Undefined()
    def divide(self, n):
        return Undefined()
two = Number(2)
twelve = Number(12)
thirteen = Number(13)

print(thirteen.value())
five = Number(5)
eight = thirteen.minus(five)
print(eight.value())
twenty_four = two.times(twelve)
print(twenty_four.value())

zero = Number(0)
one = Number(1)
something = one.divide(zero)
print(something.value())

six = twelve.divide(two)
print(six.value())

another_thing = something.plus(one)
print(another_thing.value())

yet_another_thing = one.minus(something)
print(yet_another_thing.value())


seventeen = Number(17)
four = Number(4)
zero = Number(0)

thirteen = seventeen.minus(four)
fiftytwo = thirteen.times(four)

blackjack=seventeen.plus(four)
something=blackjack.divide(zero)
another_thing=blackjack.plus(something)
something_else=another_thing.divide(blackjack)

### DUNNO
'''
qn 6a, b (power set)
Q5 pt 5 - • [20, 16, 14, 10, 8, 4, 2]
q3 bubble sort
q4 prefix infix

'''

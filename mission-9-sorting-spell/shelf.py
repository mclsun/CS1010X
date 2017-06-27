#!/usr/bin/env python3
"""

         sorting_animation.py

A minimal sorting algorithm animation:
Sorts a shelf of 10 blocks using insertion
sort, selection sort and quicksort.

Shelfs are implemented using builtin lists.

Blocks are turtles with shape "square", but
stretched to rectangles by shapesize()
 ---------------------------------------
       To exit press space button
 ---------------------------------------
"""
from turtle import *

class Block(Turtle):
    def __init__(self, size):
        self.size = size
        Turtle.__init__(self, shape="square", visible=False)
        self.pu()
        self.shapesize(size * 1.5, 1.5, 2) # square-->rectangle
        self.fillcolor("black")
        self.st()
    def glow(self):
        self.fillcolor("red")
    def unglow(self):
        self.fillcolor("black")
    def __repr__(self):
        return "Block size: {0}".format(self.size)

class Shelf(list):
    def __init__(self, y):
        "create an shelf. y is y-position of first block"
        self.y = y
        self.x = -150
    def push(self, d):
        width, _, _ = d.shapesize()
        yoffset = width/2 * 20 # to align the blocks by it's bottom edge
        d.sety(self.y + yoffset)
        d.setx(self.x+34*len(self))
        self.append(d)
    def _close_gap_from_i(self, i):
        for b in self[i:]:
            xpos, _ = b.pos()
            b.setx(xpos - 34)
    def _open_gap_from_i(self, i):
        for b in self[i:]:
            xpos, _ = b.pos()
            b.setx(xpos + 34)
    def pop(self, key):
        b = list.pop(self, key)
        b.glow()
        b.sety(200)
        self._close_gap_from_i(key)
        return b
    def insert(self, key, b):
        self._open_gap_from_i(key)
        list.insert(self, key, b)
        b.setx(self.x+34*key)
        width, _, _ = b.shapesize()
        yoffset = width/2 * 20 # to align the blocks by it's bottom edge
        b.sety(self.y + yoffset)
        b.unglow()

def show_text(text):
    goto(0,-250)
    write(text, align="center", font=("Courier", 16, "bold"))

def start_sort():
    onkey(None,"space")
    clear()
    show_text("sort_me")
    sort_func(s)

def init_shelf(vals=(4, 8, 2, 9, 3, 1, 10, 7, 5, 6)):
    s = Shelf(-200)
    for i in vals:
        s.push(Block(i))
    return s

def clear_window():
    getscreen().clearscreen()

def main(func):
    global sort_func
    sort_func = func
    getscreen().clearscreen()
    ht(); penup()
    init_shelf()
    show_text("press spacebar to start sorting")
    onkey(start_sort, "space")
    onkey(bye, "Escape")
    listen()
    mainloop()

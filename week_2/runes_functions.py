# not giving docs is a ploy to force students to revist the slides just for the arguments lol

# UNOFFICIAL DOCS

#FUNCTIONS
show(pic)
clear_all()

stack(pic1, pic2)
# => pic2 at bottom of pic1
# if want multiple stacking - 0.5, 0.25, 0.25
# stack(pic1, stack(pic1, pic2))
stack_frac(1/n, pic1, pic2)
# => pic 1 is 1/n top of the canvas, pic2 is the rest
stackn(n, pic)

quarter_turn_right(pic)
quarter_turn_left(pic)
eighth_turn_left(pic) # no eighth_turn_right

flip_horiz
flip_vert
turn_upside_down(pic)
# => quarter_turn_right(quarter_turn_right(pic))

beside(pic1, pic2)
# => pic1 on left of pic2

make_cross(pic)
# => cross shape with the bottom left corner being pic

repeat_pattern(n, pat, pic)
# eg of recursion

def repeat_pattern(n, pat, pic):
    if n == 0:
        return pic
    else:
        return pat(repeat_pattern(n-1, pat, pic))


# show(repeat_pattern(4, make_cross, heart_bb))
# => 64 hearts


#RUNES
black_bb
blank_bb
circle_bb
heart_bb
ribbon_bb
pentagram_bb


#STEREOGRAM
overlay(pic1, pic2)
overlay_prac(1/n, pic1, pic2)
# =>

#scaling
scale(1/2, pic1)
# => size, centered

stereogram(depth_map)

## to try out
overlay_prac(1/n, pic1, pic2)
show(stac_frac(1/3, pic1, pic2))
show(stackn(5, quarter_turn_right(stackn(5, quarter_turn_left(heart_bb)))))
